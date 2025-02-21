# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from .cli         import konsol
from functools    import wraps
from hashlib      import md5
from urllib.parse import urlencode
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

def normalize_for_key(value):
    """
    Cache key oluşturma amacıyla verilen değeri normalize eder.
    - Basit tipler (int, float, str, bool, None) doğrudan kullanılır.
    - dict: Anahtarları sıralı olarak normalize eder.
    - list/tuple: Elemanları normalize eder.
    - Diğer: Sadece sınıf ismi kullanılır.
    """
    if isinstance(value, (int, float, str, bool, type(None))):
        return value

    elif isinstance(value, dict):
        return {k: normalize_for_key(value[k]) for k in sorted(value)}

    elif isinstance(value, (list, tuple)):
        return [normalize_for_key(item) for item in value]

    else:
        return value.__class__.__name__

def simple_cache_key(func, args, kwargs) -> str:
    """
    Fonksiyonun tam adı ve parametrelerini kullanarak bir cache key oluşturur.
    Oluşturulan stringin sonuna MD5 hash eklenebilir.
    """
    base_key = f"{func.__module__}.{func.__qualname__}"

    if args:
        norm_args = [normalize_for_key(arg) for arg in args]
        base_key += f"|{norm_args}"

    if kwargs:
        norm_kwargs = {k: normalize_for_key(v) for k, v in kwargs.items()}
        base_key   += f"|{str(sorted(norm_kwargs.items()))}"

    hashed = md5(base_key.encode('utf-8')).hexdigest()
    return f"{base_key}"  # |{hashed}

async def make_cache_key(func, args, kwargs, is_fastapi=False) -> str:
    """
    Cache key'ini oluşturur.
    - is_fastapi=False ise simple_cache_key() kullanılır.
    - True ise FastAPI Request nesnesine göre özel key oluşturulur.
    """
    if not is_fastapi:
        return simple_cache_key(func, args, kwargs)

    # FastAPI: request ilk argümandan ya da kwargs'dan alınır.
    request = args[0] if args else kwargs.get("request")

    if request.method == "GET":
        # Eğer query_params boşsa {} olarak ayarla
        veri = dict(request.query_params) if request.query_params else {}
    else:
        try:
            veri = await request.json()
        except Exception:
            form_data = await request.form()
            veri = dict(form_data.items())

    # Eğer "kurek" gibi özel parametreler varsa temizleyebilirsiniz:
    veri.pop("kurek", None)

    args_hash = md5(urlencode(veri).encode()).hexdigest() if veri else ""
    return f"{request.url.path}?{veri}"

# -----------------------------------------------------
# Senkron Cache (RAM) Sınıfı
# -----------------------------------------------------

class SyncCache:
    """
    Senkron fonksiyonlar için basit in-memory cache.
    TTL süresi dolan veriler periyodik olarak arka plan thread’iyle temizlenir.
    """
    def __init__(self, ttl=UNLIMITED, cleanup_interval=60 * 60):
        self._ttl   = ttl
        self._data  = {}
        self._times = {}

        # TTL sınırsız değilse, cleanup_interval ile ttl'den büyük olanı kullanıyoruz.
        self._cleanup_interval = max(ttl, cleanup_interval) if ttl is not UNLIMITED else cleanup_interval

        # Arka planda çalışan ve periyodik olarak expired entry'leri temizleyen thread başlatılıyor.
        self._lock           = threading.RLock()
        self._cleanup_thread = threading.Thread(target=self._auto_cleanup, daemon=True)
        self._cleanup_thread.start()

    def _auto_cleanup(self):
        """Belirlenen aralıklarla cache içerisindeki süresi dolmuş entry'leri temizler."""
        while True:
            time.sleep(self._cleanup_interval)
            with self._lock:
                keys = list(self._data.keys())
                for key in keys:
                    self.remove_if_expired(key)

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
                # konsol.log(f"[red][-] {key}")

    def __getitem__(self, key):
        with self._lock:
            self.remove_if_expired(key)
            veri = self._data[key]
            # konsol.log(f"[yellow][~] {key}")
            return veri

    def __setitem__(self, key, value):
        with self._lock:
            self._data[key] = value
            if self._ttl is not UNLIMITED:
                self._times[key] = time.time()

class HybridSyncCache:
    """
    Senkron işlemler için, öncelikle Redis cache kullanılmaya çalışılır.
    Redis'ten veri alınamazsa ya da hata oluşursa, SyncCache (in-memory) fallback uygulanır.
    """
    def __init__(self, ttl=None):
        self._ttl = ttl

        try:
            self.redis = redis.Redis(
                host             = REDIS_HOST,
                port             = REDIS_PORT,
                db               = REDIS_DB,
                password         = REDIS_PASS,
                decode_responses = False
            )
            self.redis.ping()
        except Exception:
            self.redis = None

        self.memory = SyncCache(ttl)

    def get(self, key):
        # Önce Redis ile deniyoruz:
        if self.redis:
            try:
                data = self.redis.get(key)
            except Exception:
                data = None
            if data is not None:
                try:
                    result = pickle.loads(data)
                    # konsol.log(f"[yellow][~] {key}")
                    return result
                except Exception:
                    # Deserialize hatası durumunda fallback'e geç
                    pass

        # Redis'te veri yoksa, yerel cache'ten alıyoruz.
        try:
            return self.memory[key]
        except KeyError:
            raise KeyError(key)

    def set(self, key, value):
        try:
            ser = pickle.dumps(value)
        except Exception:
            # Serialization hatası durumunda yerel cache'e yazalım.
            self.memory[key] = value
            return

        if self.redis:
            try:
                if self._ttl is not None:
                    self.redis.set(key, ser, ex=self._ttl)
                else:
                    self.redis.set(key, ser)
                return
            except Exception:
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
    def __init__(self, ttl=UNLIMITED, cleanup_interval=60 * 60):
        """
        :param ttl: Her entry için geçerli süre (saniye). Örneğin 3600 saniye 1 saattir.
        :param cleanup_interval: Otomatik temizleme görevinin kaç saniyede bir çalışacağını belirler.
        """
        self._ttl    = ttl
        self._data   = {}
        self._times  = {}
        self.futures = {}

        # TTL sınırsız değilse, cleanup_interval ile ttl'den büyük olanı kullanıyoruz.
        self._cleanup_interval = max(ttl, cleanup_interval) if ttl is not UNLIMITED else cleanup_interval

        # Aktif bir event loop varsa otomatik temizlik görevini başlatıyoruz.
        try:
            self._cleanup_task = asyncio.get_running_loop().create_task(self._auto_cleanup())
        except RuntimeError:
            self._cleanup_task = None

    async def _auto_cleanup(self):
        """Belirlenen aralıklarla cache içerisindeki süresi dolmuş entry'leri temizler."""
        while True:
            await asyncio.sleep(self._cleanup_interval)
            for key in list(self._data.keys()):
                self.remove_if_expired(key)

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
                # konsol.log(f"[red][-] {key}")
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
            # konsol.log(f"[yellow][~] {key}")
            return value
        except KeyError:
            # Eğer key cache'de yoksa, aynı key ile başlatılmış future varsa onu bekle.
            future = self.futures.get(key)
            if future:
                await future
                # Future tamamlandığında sonucu döndür.
                value = future.result()
                # konsol.log(f"[yellow][?] {key}")
                return value
            # Eğer future da yoksa, key bulunamadığına dair hata fırlat.
            raise KeyError(key)

    async def set(self, key, value):
        """Belirtilen key için cache'e değer ekler."""
        self.ensure_cleanup_task()
        self._data[key] = value
        if self._ttl is not UNLIMITED:
            self._times[key] = time.time()

class HybridAsyncCache:
    """
    Öncelikle Redis cache kullanılmaya çalışılır.
    Hata durumunda veya Redis erişilemiyorsa in-memory AsyncCache’e geçilir.
    """
    def __init__(self, ttl=UNLIMITED):
        self._ttl = ttl

        try:
            self.redis = redisAsync.Redis(
                host             = REDIS_HOST,
                port             = REDIS_PORT,
                db               = REDIS_DB,
                password         = REDIS_PASS,
                decode_responses = False
            )
        except Exception:
            self.redis = None

        self.memory  = AsyncCache(ttl)
        self.futures = {}

    async def get(self, key):
        # Eşzamanlı istek yönetimi: aynı key için bir future varsa, direkt bekleyip sonucu döndür.
        if key in self.futures:
            # konsol.log(f"[yellow][?] {key}")
            return await self.futures[key]

        # İlk önce Redis ile deneyelim
        if self.redis:
            try:
                data = await self.redis.get(key)
            except Exception:
                return await self.memory.get(key)
            if data is not None:
                try:
                    result = pickle.loads(data)
                    # konsol.log(f"[yellow][~] {key}")
                    return result
                except Exception:
                    # Deserialize hatası durumunda in-memory cache'ten dene
                    return await self.memory.get(key)
            else:
                # Redis'te veri yoksa, in-memory cache'e bak
                return await self.memory.get(key)
        else:
            # Redis kullanılmıyorsa doğrudan in-memory cache'e bak
            return await self.memory.get(key)

    async def set(self, key, value):
        # Önce veriyi pickle etmeyi deniyoruz.
        try:
            ser = pickle.dumps(value)
        except Exception:
            # Serialization hatası durumunda sadece in-memory cache'e yaz
            await self.memory.set(key, value)
            return

        if self.redis:
            try:
                if self._ttl is not UNLIMITED:
                    await self.redis.set(key, ser, ex=self._ttl)
                else:
                    await self.redis.set(key, ser)
                return
            except Exception:
                # Redis yazma hatası durumunda in-memory fallback
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
        # konsol.log(f"[green][+] {key}")

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

        # unless koşuluna göre cache'e ekleme yap.
        if unless is None or not unless(result):
            await cache.set(key, result)
            # konsol.log(f"[green][+] {key}")

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

def kekik_cache(ttl=UNLIMITED, unless=None, is_fastapi=False, use_redis=True):
    """
    Bir fonksiyonun (senkron/asenkron) sonucunu cache'ler.
    
    Parametreler:
      - ttl: Cache'in geçerlilik süresi (saniye). UNLIMITED ise süresizdir.
      - unless: Sonuç alınmadan önce çağrılan, True dönerse cache'e alınmaz.
      - is_fastapi: True ise, FastAPI Request nesnesine göre key oluşturur.
      - use_redis: Asenkron fonksiyonlarda Redis kullanımı (Hybrid cache) için True verilebilir.
    
    Örnek Kullanım:
    
        @kekik_cache(ttl=15, unless=lambda sonuc: sonuc is None)
        async def bakalim(param):
            return param
    """
    # Parametresiz kullanım durumunda
    if callable(ttl):
        return kekik_cache(UNLIMITED, unless=unless, is_fastapi=is_fastapi, use_redis=use_redis)(ttl)

    def decorator(func):
        if asyncio.iscoroutinefunction(func):
            # Asenkron fonksiyonlar için cache türünü seçelim:

            func.__cache = HybridAsyncCache(ttl) if use_redis else AsyncCache(ttl)

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                key = await make_cache_key(func, args, kwargs, is_fastapi)

                try:
                    return await func.__cache.get(key)
                except KeyError:
                    return await _async_compute_and_cache(func, key, unless, *args, **kwargs)

            return async_wrapper
        else:
            # Senkron fonksiyonlar için
            func.__cache = HybridSyncCache(ttl) if use_redis else SyncCache(ttl)

            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                key = simple_cache_key(func, args, kwargs)

                try:
                    return func.__cache[key]
                except KeyError:
                    result = func(*args, **kwargs)
                    _sync_maybe_cache(func, key, result, unless)
                    return result

            return sync_wrapper

    return decorator