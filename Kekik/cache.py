# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from .cli         import konsol
from functools    import wraps
from hashlib      import md5
from inspect      import signature
import json
import time
import threading
import asyncio
import pickle

# Redis client (Redis yoksa fallback yapılacak)
import redis.asyncio as redisAsync
import redis         as redis

# -----------------------------------------------------
# Sabitler ve Yardımcı Fonksiyonlar
# -----------------------------------------------------
UNLIMITED  = None

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB   = 0
REDIS_PASS = None

def _is_json_serializable(value):
    """Verinin JSON'a serileştirilebilir olup olmadığını kontrol eder."""
    try:
        json.dumps(value)
        return True
    except (TypeError, ValueError):
        return False

def _serialize_for_cache(value):
    """
    Veriyi cache'e yazmak için serialize eder.
    JSON serileştirilebilirse JSON kullanır (hafif, hızlı).
    Yoksa pickle kullanır (ağır, kompleks objeler için).
    
    Format:
    - JSON: 0x01 + json_bytes (1 byte header + JSON data)
    - Pickle: 0x02 + pickle_bytes (1 byte header + Pickle data)
    - Eski format (sadece pickle): pickle_bytes (uyumluluğu için)
    """
    if _is_json_serializable(value):
        # JSON: 0x01 marker + json_data
        json_bytes = json.dumps(value).encode('utf-8')
        return b'\x01' + json_bytes
    else:
        # Pickle: 0x02 marker + pickle_data
        pickle_bytes = pickle.dumps(value)
        return b'\x02' + pickle_bytes

def _deserialize_from_cache(data):
    """Cache'ten okunan veriyi deserialize eder."""
    if not isinstance(data, bytes):
        # Tuple format (eski compat) - tuple döndürüldüyse
        if isinstance(data, tuple) and len(data) == 2:
            format_type, serialized = data
            if format_type == b'JSON':
                return json.loads(serialized.decode('utf-8'))
            elif format_type == b'PKL':
                return pickle.loads(serialized)
        # Fallback: pickle dene
        return pickle.loads(data)
    
    # Yeni format: ilk byte format marker
    if len(data) > 0:
        marker = data[0:1]
        payload = data[1:]
        
        if marker == b'\x01':
            # JSON format
            return json.loads(payload.decode('utf-8'))
        elif marker == b'\x02':
            # Pickle format
            return pickle.loads(payload)
    
    # Formatı tanımıyorsa, eski format (sadece pickle) olabilir
    try:
        return pickle.loads(data)
    except Exception:
        # Son çare: tuple format?
        if isinstance(data, tuple) and len(data) == 2:
            format_type, serialized = data
            if format_type == b'JSON':
                return json.loads(serialized.decode('utf-8'))
            elif format_type == b'PKL':
                return pickle.loads(serialized)
        raise

def normalize_for_key(value):
    """
    Cache key oluşturma amacıyla verilen değeri normalize eder.
    - Basit tipler (int, float, str, bool, None) doğrudan kullanılır.
    - dict: Anahtarları sıralı olarak normalize eder.
    - list/tuple: Elemanları normalize eder.
    - Diğer: Sadece sınıf ismi kullanılır (karşılaştırılabilir objeler için).
    """
    if isinstance(value, (int, float, str, bool, type(None))):
        return value

    elif isinstance(value, dict):
        return {k: normalize_for_key(value[k]) for k in sorted(value)}

    elif isinstance(value, (list, tuple)):
        return [normalize_for_key(item) for item in value]

    else:
        # Kompleks objeler için: önce __str__ veya __repr__ dene, yoksa class name
        try:
            # Eğer obje anlamlı bir string representation'a sahipse kullan
            str_repr = str(value)
            # Çok uzun string'leri (>100 karakter) sadece class name'e indir
            if len(str_repr) < 100 and not str_repr.startswith('<'):
                return str_repr
        except:
            pass
        
        return value.__class__.__name__

def simple_cache_key(func, args, kwargs) -> str:
    """
    Fonksiyonun tam adı ve parametrelerini kullanarak bir cache key oluşturur.
    self parametresini hariç tutar (class method'lar için).
    """
    base_key = f"{func.__module__}.{func.__qualname__}"
    base_key = "|".join(base_key.split("."))

    # Fonksiyon signature'ını kontrol et ve self/cls parametresini tespit et
    filtered_args = args
    try:
        sig = signature(func)
        params = list(sig.parameters.keys())
        # İlk parametre 'self' veya 'cls' ise, args'ın ilk elemanını hariç tut
        if params and len(params) > 0 and params[0] in ('self', 'cls') and len(args) > 0:
            filtered_args = args[1:]
    except (ValueError, TypeError):
        # signature() başarısız olursa args'ı olduğu gibi kullan
        pass

    # Sadece filtered_args gerçekten doluysa ekle (boş tuple/list değilse)
    if filtered_args and len(filtered_args) > 0:
        norm_args = [normalize_for_key(arg) for arg in filtered_args]
        base_key += f"|{norm_args}"

    if kwargs:
        norm_kwargs = {k: normalize_for_key(v) for k, v in kwargs.items()}
        base_key   += f"|{str(sorted(norm_kwargs.items()))}"

    hashed = md5(base_key.encode('utf-8')).hexdigest()
    return f"{base_key}"  # |{hashed}

# -----------------------------------------------------
# Senkron Cache (RAM) Sınıfı
# -----------------------------------------------------

class SyncCache:
    """
    Senkron fonksiyonlar için basit in-memory cache.
    TTL süresi dolan veriler periyodik olarak arka plan thread'iyle temizlenir.
    """
    def __init__(self, ttl=UNLIMITED, cleanup_interval=60 * 60, max_size=10000):
        self._ttl           = ttl
        self._data          = {}
        self._times         = {}
        self._access_counts = {}  # LRU tracker
        self._max_size      = max_size

        # TTL sınırsız değilse, cleanup_interval kullanıyoruz.
        self._cleanup_interval = cleanup_interval if ttl is UNLIMITED else min(ttl, cleanup_interval)

        # Arka planda çalışan ve periyodik olarak expired entry'leri temizleyen thread başlatılıyor.
        self._lock                  = threading.RLock()
        self._cleanup_thread        = threading.Thread(target=self._auto_cleanup, daemon=True)
        self._cleanup_thread.daemon = True
        self._cleanup_thread.start()

    def _auto_cleanup(self):
        """Belirlenen aralıklarla cache içerisindeki süresi dolmuş entry'leri temizler."""
        while True:
            try:
                time.sleep(self._cleanup_interval)
                with self._lock:
                    keys = list(self._data.keys())
                    for key in keys:
                        self.remove_if_expired(key)
            except Exception as e:
                konsol.log(f"[red]Cache cleanup hatası: {e}")

    def _is_expired(self, key):
        """Belirtilen key'in süresi dolmuşsa True döner."""
        if self._ttl is UNLIMITED:
            return False

        timestamp = self._times.get(key)

        return timestamp is not None and (time.time() - timestamp > self._ttl)

    def remove_if_expired(self, key):
        """
        Eğer key'in cache süresi dolmuşsa, ilgili entry'yi temizler.
        Thread güvenliği sağlamak için lock kullanılır.
        """
        with self._lock:
            if self._is_expired(key):
                self._data.pop(key, None)
                self._times.pop(key, None)
                # konsol.log(f"[red][-] {str(key)[:100]}")

    def __getitem__(self, key):
        with self._lock:
            self.remove_if_expired(key)
            veri = self._data[key]
            # LRU tracker'ı güncelle
            self._access_counts[key] = self._access_counts.get(key, 0) + 1
            # konsol.log(f"[yellow][~] {str(key)[:100]}")
            return veri

    def __setitem__(self, key, value):
        with self._lock:
            # Kapasite kontrolü - LRU temizlemesi
            if len(self._data) >= self._max_size and key not in self._data:
                # En az kullanılan key'i bul ve sil
                lru_key = min(self._access_counts, key=self._access_counts.get)
                self._data.pop(lru_key, None)
                self._times.pop(lru_key, None)
                self._access_counts.pop(lru_key, None)
                # konsol.log(f"[red][-] LRU eviction: {lru_key}")

            self._data[key]          = value
            self._access_counts[key] = 0
            if self._ttl is not UNLIMITED:
                self._times[key] = time.time()

class HybridSyncCache:
    """
    Senkron işlemler için, öncelikle Redis cache kullanılmaya çalışılır.
    Redis'ten veri alınamazsa ya da hata oluşursa, SyncCache (in-memory) fallback uygulanır.
    """
    def __init__(self, ttl=None, max_size=10000):
        self._ttl = ttl
        self._max_size = max_size

        try:
            self.redis = redis.Redis(
                host             = REDIS_HOST,
                port             = REDIS_PORT,
                db               = REDIS_DB,
                password         = REDIS_PASS,
                decode_responses = False
            )
            self.redis.ping()
        except Exception as e:
            konsol.log(f"[yellow]Redis bağlantısı başarısız, in-memory cache kullanılıyor: {e}")
            self.redis = None

        self.memory = SyncCache(ttl, max_size=max_size)

    def get(self, key):
        # Önce Redis ile deniyoruz:
        if self.redis:
            try:
                data = self.redis.get(key)
            except Exception as e:
                data = None
            if data is not None:
                try:
                    result = _deserialize_from_cache(data)
                    return result
                except Exception as e:
                    # Deserialize hatası durumunda fallback'e geç
                    pass

        # Redis'te veri yoksa, yerel cache'ten alıyoruz.
        try:
            return self.memory[key]
        except KeyError:
            raise KeyError(key)

    def set(self, key, value):
        # Veriyi serialize et (JSON tercih, yoksa pickle)
        serialized = _serialize_for_cache(value)

        if self.redis:
            try:
                if self._ttl is not None:
                    self.redis.set(key, serialized, ex=self._ttl)
                else:
                    self.redis.set(key, serialized)
                return
            except Exception as e:
                # Redis'e yazılamazsa yerel cache'e geçelim.
                self.memory[key] = value
                return
        else:
            # Redis kullanılmıyorsa direkt yerel cache'e yaz.
            self.memory[key] = value

    # HybridSyncCache'in subscriptable olması için:
    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

# -----------------------------------------------------
# Asenkron Cache (In-Memory) ve Redis Hybrid Cache
# -----------------------------------------------------

class AsyncCache:
    """
    Temel in-memory asenkron cache.
    """
    def __init__(self, ttl=UNLIMITED, cleanup_interval=60 * 60, max_size=10000):
        """
        :param ttl: Her entry için geçerli süre (saniye). Örneğin 3600 saniye 1 saattir.
        :param cleanup_interval: Otomatik temizleme görevinin kaç saniyede bir çalışacağını belirler.
        :param max_size: Maksimum cache boyutu (en eski entry'ler silinir).
        """
        self._ttl           = ttl
        self._data          = {}
        self._times         = {}
        self._access_counts = {}  # LRU tracker
        self.futures        = {}
        self._max_size      = max_size

        # TTL sınırsız değilse, cleanup_interval kullanıyoruz.
        self._cleanup_interval = cleanup_interval if ttl is UNLIMITED else min(ttl, cleanup_interval)

        # Aktif bir event loop varsa otomatik temizlik görevini başlatıyoruz.
        try:
            self._cleanup_task = asyncio.get_running_loop().create_task(self._auto_cleanup())
        except RuntimeError:
            self._cleanup_task = None

    async def _auto_cleanup(self):
        """Belirlenen aralıklarla cache içerisindeki süresi dolmuş entry'leri temizler."""
        while True:
            try:
                await asyncio.sleep(self._cleanup_interval)
                for key in list(self._data.keys()):
                    self.remove_if_expired(key)
            except Exception as e:
                konsol.log(f"[red]Async cache cleanup hatası: {e}")

    def ensure_cleanup_task(self):
        """Event loop mevcutsa, cleanup task henüz başlatılmadıysa oluştur."""
        if self._cleanup_task is None:
            try:
                self._cleanup_task = asyncio.get_running_loop().create_task(self._auto_cleanup())
            except RuntimeError:
                pass  # Yine loop yoksa yapacak bir şey yok

    def remove_if_expired(self, key):
        """
        Belirtilen key'in süresi dolduysa, cache ve futures içerisinden temizler.
        """
        if self._ttl is not UNLIMITED:
            t = self._times.get(key)
            if t is not None and (time.time() - t > self._ttl):
                # konsol.log(f"[red][-] Expired: {str(key)[:100]}")
                self._data.pop(key, None)
                self._times.pop(key, None)
                self.futures.pop(key, None)

    async def get(self, key):
        """
        Belirtilen key için cache'de saklanan değeri asenkron olarak döndürür.
        Eğer key bulunamazsa, ilgili future üzerinden beklemeyi sağlar.
        """
        # Cleanup task'in aktif olduğundan emin olun.
        self.ensure_cleanup_task()
        # Eğer key'in süresi dolmuşsa, kaldırın.
        self.remove_if_expired(key)

        try:
            # Cache içerisinde key varsa direkt değeri döndür.
            value = self._data[key]
            # LRU tracker'ı güncelle
            self._access_counts[key] = self._access_counts.get(key, 0) + 1
            # konsol.log(f"[yellow][~] {str(key)[:100]}")
            return value
        except KeyError:
            # Eğer key cache'de yoksa, aynı key ile başlatılmış future varsa onu bekle.
            future = self.futures.get(key)
            if future:
                await future
                # Future tamamlandığında sonucu döndür.
                value = future.result()
                # konsol.log(f"[yellow][?] {str(key)[:100]}")
                return value
            # Eğer future da yoksa, key bulunamadığına dair hata fırlat.
            raise KeyError(key)

    async def set(self, key, value):
        """Belirtilen key için cache'e değer ekler."""
        self.ensure_cleanup_task()

        # Kapasite kontrolü - LRU temizlemesi
        if len(self._data) >= self._max_size and key not in self._data:
            # En az kullanılan key'i bul ve sil
            lru_key = min(self._access_counts, key=self._access_counts.get)
            self._data.pop(lru_key, None)
            self._times.pop(lru_key, None)
            self._access_counts.pop(lru_key, None)
            self.futures.pop(lru_key, None)
            # konsol.log(f"[red][-] Async LRU eviction: {lru_key}")

        self._data[key]          = value
        self._access_counts[key] = 0
        if self._ttl is not UNLIMITED:
            self._times[key] = time.time()

class HybridAsyncCache:
    """
    Öncelikle Redis cache kullanılmaya çalışılır.
    Hata durumunda veya Redis erişilemiyorsa in-memory AsyncCache'e geçilir.
    """
    def __init__(self, ttl=UNLIMITED, max_size=10000):
        self._ttl = ttl
        self._max_size = max_size

        try:
            self.redis = redisAsync.Redis(
                host             = REDIS_HOST,
                port             = REDIS_PORT,
                db               = REDIS_DB,
                password         = REDIS_PASS,
                decode_responses = False
            )
        except Exception as e:
            konsol.log(f"[yellow]Async Redis bağlantısı başarısız, in-memory cache kullanılıyor: {e}")
            self.redis = None

        self.memory  = AsyncCache(ttl, max_size=max_size)
        self.futures = {}

    async def get(self, key):
        # Eşzamanlı istek yönetimi: aynı key için bir future varsa, direkt bekleyip sonucu döndür.
        if key in self.futures:
            # konsol.log(f"[yellow][?] {str(key)[:100]}")
            return await self.futures[key]

        # İlk önce Redis ile deneyelim
        if self.redis:
            try:
                data = await self.redis.get(key)
            except Exception as e:
                konsol.log(f"[yellow]Async Redis get hatası: {e}")
                return await self.memory.get(key)
            if data is not None:
                try:
                    result = _deserialize_from_cache(data)
                    # konsol.log(f"[yellow][~] {str(key)[:100]}")
                    return result
                except Exception as e:
                    # Deserialize hatası durumunda in-memory cache'ten dene
                    konsol.log(f"[yellow]Async deserialize hatası: {e}")
                    return await self.memory.get(key)
            else:
                # Redis'te veri yoksa, in-memory cache'e bak
                return await self.memory.get(key)
        else:
            # Redis kullanılmıyorsa doğrudan in-memory cache'e bak
            return await self.memory.get(key)

    async def set(self, key, value):
        # Veriyi serialize et (JSON tercih, yoksa pickle)
        serialized = _serialize_for_cache(value)

        if self.redis:
            try:
                if self._ttl is not UNLIMITED:
                    await self.redis.set(key, serialized, ex=self._ttl)
                else:
                    await self.redis.set(key, serialized)
                return
            except Exception as e:
                # Redis yazma hatası durumunda in-memory fallback
                # konsol.log(f"[yellow]Async Redis set hatası: {e}, in-memory cache kullanılıyor")
                await self.memory.set(key, value)
                return
        else:
            # Redis yoksa in-memory cache'e yaz
            await self.memory.set(key, value)

# -----------------------------------------------------
# Cache'e Hesaplanmış Sonucu Yazma Yardımcı Fonksiyonları
# -----------------------------------------------------

def _sync_maybe_cache(func, key, result, unless):
    """Senkron fonksiyon sonucu için cache kaydı oluşturur."""
    if unless is None or not unless(result):
        func.__cache[key] = result
        # konsol.log(f"[green][+] {str(key)[:100]}")

async def _async_compute_and_cache(func, key, unless, *args, **kwargs):
    """
    Asenkron fonksiyon sonucunu hesaplar ve cache'e yazar.
    Aynı key için gelen eşzamanlı çağrılar future üzerinden bekletilir.
    """
    # __cache'den cache nesnesini alıyoruz.
    cache = func.__cache

    # Aynı key için aktif bir future varsa, onun sonucunu döndür.
    if key in cache.futures:
        return await cache.futures[key]

    # Yeni future oluşturuluyor ve cache.futures'e ekleniyor.
    future             = asyncio.Future()
    cache.futures[key] = future

    try:
        # Asenkron fonksiyonu çalıştır ve sonucu elde et.
        result = await func(*args, **kwargs)
        future.set_result(result)

        # unless koşuluna göre cache'e ekleme yap
        if unless is None or not unless(result):
            await cache.set(key, result)
            # konsol.log(f"[green][+] {str(key)[:100]}")

        return result
    except Exception as exc:
        future.cancel()
        raise exc
    finally:
        # İşlem tamamlandığında future'ı temizle.
        cache.futures.pop(key, None)

# -----------------------------------------------------
# kekik_cache Dekoratörü (Senkrondan Asenkrona)
# -----------------------------------------------------

def kekik_cache(ttl=UNLIMITED, unless=None, use_redis=True, max_size=10000, is_fastapi=False):
    """
    Bir fonksiyonun (senkron/asenkron) sonucunu cache'ler.
    
    Parametreler:
      - ttl: Cache'in geçerlilik süresi (saniye). UNLIMITED ise süresizdir.
      - unless: Sonuç alınmadan önce çağrılan, True dönerse cache'e alınmaz.
      - use_redis: Redis kullanımı (True = Redis + in-memory fallback, False = in-memory sadece).
      - max_size: Cache'in maksimum boyutu. Kapasiteyi aşarsa LRU temizlemesi yapılır.
      - is_fastapi: FastAPI uyumluluğu (True ise cache'leme yapılmaz, geriye dönük uyumluluk için).
    
    Örnek Kullanım:
    
        # Basit fonksiyon (sync)
        @kekik_cache(ttl=300)
        def hesapla(x, y):
            return x + y
        
        # Asenkron fonksiyon
        @kekik_cache(ttl=600)
        async def veri_al(id):
            return await db.fetch(id)
        
        # İç fonksiyonlar (class method)
        class Veritabani:
            @kekik_cache(ttl=3600)
            async def get_user(self, user_id):
                return await self.db.get_user(user_id)
        
        # Koşullu cache'leme (hata response'larını cache'leme)
        @kekik_cache(ttl=300, unless=lambda r: r.get("error") is not None)
        async def api_call():
            return {"data": "..."}
    """
    # is_fastapi=True ise cache'lemeyi devre dışı bırak
    if is_fastapi:
        def no_cache_decorator(func):
            return func
        return no_cache_decorator
    
    # Parametresiz kullanım durumunda
    if callable(ttl):
        return kekik_cache(UNLIMITED, unless=unless, use_redis=use_redis, max_size=max_size, is_fastapi=is_fastapi)(ttl)

    def decorator(func):
        if asyncio.iscoroutinefunction(func):
            # Asenkron fonksiyonlar için cache türünü seçelim:
            func.__cache = HybridAsyncCache(ttl, max_size=max_size) if use_redis else AsyncCache(ttl, max_size=max_size)

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                key = simple_cache_key(func, args, kwargs)

                try:
                    cached = await func.__cache.get(key)
                    # konsol.log(f"[blue]CACHE HIT[/blue]: {str(key)[:100]}")
                    return cached
                except KeyError:
                    # konsol.log(f"[magenta]CACHE MISS[/magenta]: {str(key)[:100]}")
                    return await _async_compute_and_cache(func, key, unless, *args, **kwargs)

            return async_wrapper
        else:
            # Senkron fonksiyonlar için
            func.__cache = HybridSyncCache(ttl, max_size=max_size) if use_redis else SyncCache(ttl, max_size=max_size)

            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                key = simple_cache_key(func, args, kwargs)

                try:
                    cached = func.__cache[key]
                    # konsol.log(f"[blue]CACHE HIT[/blue]: {str(key)[:100]}")
                    return cached
                except KeyError:
                    # konsol.log(f"[magenta]CACHE MISS[/magenta]: {str(key)[:100]}")
                    result = func(*args, **kwargs)
                    _sync_maybe_cache(func, key, result, unless)
                    return result

            return sync_wrapper

    return decorator