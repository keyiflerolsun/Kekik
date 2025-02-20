# ! https://github.com/Fatal1ty/aiocached

from .cli         import konsol
from functools    import wraps
from time         import time, sleep
from hashlib      import md5
from urllib.parse import urlencode
import asyncio, threading

# -----------------------------------------------------
# Yardımcı Fonksiyonlar
# -----------------------------------------------------

UNLIMITED = None

def normalize_for_key(value):
    """
    Cache key oluşturma amacıyla verilen değeri normalize eder.
    - Basit tipler (int, float, str, bool, None) direk kullanılır.
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
    Oluşturulan stringin sonuna MD5 hash eklenir.
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

    # FastAPI: request ilk argüman ya da kwargs'dan alınır
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

    args_hash = md5(urlencode(veri).encode()).hexdigest() if veri else ""
    return f"{request.url.path}?{veri}"


# -----------------------------------------------------
# In-Memory (RAM) Cache
# -----------------------------------------------------

class Cache:
    def __init__(self, ttl=UNLIMITED):
        self._ttl   = ttl
        self._data  = {}
        self._times = {}

    def _is_expired(self, key):
        """Belirtilen key'in süresi dolmuşsa True döner."""
        if self._ttl is UNLIMITED:
            return False

        timestamp = self._times.get(key)

        return timestamp is not None and (time() - timestamp > self._ttl)


class SyncCache(Cache):
    """
    Basit in-memory cache yapısı.
    TTL (time-to-live) süresi dolan veriler otomatik olarak temizlenir.
    Bu versiyonda, otomatik temizleme işlevselliği bir thread ile sağlanır.
    """
    def __init__(self, ttl=UNLIMITED, cleanup_interval=60 * 60):
        super().__init__(ttl)

        # TTL sınırsız değilse, cleanup_interval ile ttl'den büyük olanı kullanıyoruz.
        self._cleanup_interval = max(ttl, cleanup_interval) if ttl is not UNLIMITED else cleanup_interval
        self._lock = threading.RLock()

        # Arka planda çalışan ve periyodik olarak expired entry'leri temizleyen thread başlatılıyor.
        self._cleanup_thread = threading.Thread(target=self._auto_cleanup, daemon=True)
        self._cleanup_thread.start()

    def _auto_cleanup(self):
        """Belirlenen aralıklarla cache içerisindeki süresi dolmuş entry'leri temizler."""
        while True:
            sleep(self._cleanup_interval)
            with self._lock:
                keys = list(self._data.keys())
                for key in keys:
                    self.remove_if_expired(key)

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
            # konsol.log(f"[green][+] {key}")
            if self._ttl is not UNLIMITED:
                self._times[key] = time()


class AsyncCache(Cache):
    """
    Asenkron işlemleri destekleyen cache yapısı.
    Aynı key için gelen eşzamanlı çağrılar, futures kullanılarak tek sonuç üzerinden paylaşılır.
    Ek olarak, belirli aralıklarla cache’i kontrol edip, süresi dolmuş verileri temizleyen otomatik temizleme görevi çalışır.
    """
    def __init__(self, ttl=UNLIMITED, cleanup_interval=60 * 60):
        """
        :param ttl: Her entry için geçerli süre (saniye). Örneğin 3600 saniye 1 saattir.
        :param cleanup_interval: Otomatik temizleme görevinin kaç saniyede bir çalışacağını belirler.
        """
        super().__init__(ttl)
        self.futures = {}

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
            # _data kopyasını almak, üzerinde dönüp silme yaparken hata almamak için.
            keys = list(self._data.keys())
            for key in keys:
                self.remove_if_expired(key)

    def ensure_cleanup_task(self):
        """Event loop mevcutsa, cleanup task henüz başlatılmadıysa oluştur."""
        if self._cleanup_task is None:
            try:
                self._cleanup_task = asyncio.get_running_loop().create_task(self._auto_cleanup())
            except RuntimeError:
                pass  # Yine loop yoksa yapacak bir şey yok

    async def get(self, key):
        """
        Belirtilen key için cache'de saklanan değeri asenkron olarak döndürür.
        Eğer key bulunamazsa, ilgili future üzerinden beklemeyi sağlar.
        """
        self.ensure_cleanup_task()
        self.remove_if_expired(key)

        try:
            veri = self._data[key]
            # konsol.log(f"[yellow][~] {key}")
            return veri
        except KeyError as e:
            future = self.futures.get(key)
            if future:
                await future
                veri = future.result()
                # konsol.log(f"[yellow][?] {key}")
                return veri

            raise e

    def remove_if_expired(self, key):
        """
        Belirtilen key'in süresi dolduysa, cache ve futures içerisinden temizler.
        """
        if self._ttl is not UNLIMITED and self._is_expired(key):
            # konsol.log(f"[red][-] {key}")
            self._data.pop(key, None)
            self._times.pop(key, None)
            self.futures.pop(key, None)

    def __setitem__(self, key, value):
        self._data[key] = value
        if self._ttl is not UNLIMITED:
            self._times[key] = time()


# -----------------------------------------------------
# Fonksiyonun Sonucunu Hesaplayıp Cache'e Yazma
# -----------------------------------------------------

def _sync_maybe_cache(func, key, result, unless):
    """Senkron sonuç için cache kaydını oluşturur (unless koşuluna bakarak)."""
    if unless is None or not unless(result):
        func.__cache[key] = result
        # konsol.log(f"[green][+] {key}")

async def _async_compute_and_cache(func, key, unless, *args, **kwargs):
    """
    Asenkron fonksiyon sonucunu hesaplar ve cache'e ekler.
    Aynı key için işlem devam ediyorsa, mevcut sonucu bekler.
    Sonuç, unless(result) True değilse cache'e eklenir.
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
            cache[key] = result
            # konsol.log(f"[green][+] {key}")
        
        return result
    except Exception as exc:
        future.cancel()
        raise exc
    finally:
        # İşlem tamamlandığında future'ı temizle.
        cache.futures.pop(key, None)


# -----------------------------------------------------
# Dekoratör: kekik_cache
# -----------------------------------------------------

def kekik_cache(ttl=UNLIMITED, unless=None, is_fastapi=False):
    """
    Bir fonksiyon veya coroutine'in sonucunu cache'ler.

    Args:
        ttl (int, optional): Cache’in geçerlilik süresi (saniye). 
                                       Eğer `UNLIMITED` ise süresizdir. Varsayılan olarak `UNLIMITED`'dir.
        unless (callable, optional): Fonksiyonun sonucunu argüman olarak alan bir callable. 
                                               Eğer `True` dönerse, sonuç cache'e alınmaz. Varsayılan olarak `None`'dır.
        is_fastapi (bool, optional): Eğer `True` ise, cache key'i oluştururken FastAPI request nesnesine özel şekilde davranır.
                                     Varsayılan olarak `False`'tır.

    Notlar:
    -------
    Normalde yalnızca Redis cache kullanılmak istenir.
    Ancak Redis'e ulaşılamayan durumlarda RAM fallback kullanılır.

    ---

    Örn.:
    
        @kekik_cache(ttl=15, unless=lambda sonuc: bool(sonuc is None))
        async def bakalim(param):
            # Burada cache işlemi yapılır.
            return param
    """
    # Parametresiz kullanıldığında
    if callable(ttl):
        return kekik_cache(UNLIMITED, unless=unless, is_fastapi=is_fastapi)(ttl)

    def decorator(func):
        if asyncio.iscoroutinefunction(func):
            func.__cache = AsyncCache(ttl)

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                key = await make_cache_key(func, args, kwargs, is_fastapi)

                try:
                    return await func.__cache.get(key)
                except KeyError:
                    return await _async_compute_and_cache(func, key, unless, *args, **kwargs)

            return async_wrapper
        else:
            func.__cache = SyncCache(ttl)

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