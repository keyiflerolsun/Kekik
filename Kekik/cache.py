# ! https://github.com/Fatal1ty/aiocached

import asyncio
from functools    import wraps
from time         import time
from hashlib      import md5
from urllib.parse import urlencode

UNLIMITED = None

class Cache:
    """
    Basit in-memory cache yapısı.
    TTL (time-to-live) süresi dolan veriler otomatik olarak temizlenir.
    """
    def __init__(self, ttl=UNLIMITED):
        self._data  = {}
        self._ttl   = ttl
        self._times = {}

    def _is_expired(self, key):
        """Belirtilen key'in süresi dolduysa True döner."""
        if self._ttl is UNLIMITED:
            return False

        timestamp = self._times.get(key)

        return timestamp is not None and (time() - timestamp > self._ttl)

    def remove_if_expired(self, key):
        """
        Eğer key'in cache süresi dolmuşsa, ilgili entry'yi temizler.
        """
        if self._is_expired(key):
            self._data.pop(key, None)
            self._times.pop(key, None)

    def __getitem__(self, key):
        self.remove_if_expired(key)
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value
        if self._ttl is not UNLIMITED:
            self._times[key] = time()


class AsyncCache(Cache):
    """
    Asenkron işlemleri destekleyen cache yapısı.
    Aynı key için gelen eşzamanlı çağrılar, futures kullanılarak tek sonuç üzerinden paylaşılır.
    """
    def __init__(self, ttl=UNLIMITED):
        super().__init__(ttl)
        self.futures = {}

    async def get(self, key):
        """
        Belirtilen key için cache'de saklanan değeri asenkron olarak döndürür.
        Eğer key bulunamazsa, ilgili future üzerinden beklemeyi sağlar.
        """
        self.remove_if_expired(key)

        try:
            return self._data[key]
        except KeyError as e:
            future = self.futures.get(key)
            if future:
                await future
                return future.result()

            raise e

    def remove_if_expired(self, key):
        """
        Belirtilen key'in süresi dolduysa, cache ve futures içerisinden temizler.
        """
        if self._ttl is not UNLIMITED and self._is_expired(key):
            self._data.pop(key, None)
            self._times.pop(key, None)
            self.futures.pop(key, None)


def _sync_maybe_cache(func, key, result, unless):
    """Senkron sonuç için cache kaydını oluşturur (unless koşuluna bakarak)."""
    if unless is None or not unless(result):
        func.__cache[key] = result


async def _async_compute_and_cache(func, key, unless, *args, **kwargs):
    """
    Asenkron fonksiyon sonucu hesaplandıktan sonra, sonucu cache’e ekler.
    Eğer `unless` koşulu sağlanıyorsa cache kaydı atlanır.
    """
    cache              = func.__cache
    future             = asyncio.Future()
    cache.futures[key] = future

    try:
        result = await func(*args, **kwargs)
    except Exception as exc:
        cache.futures.pop(key, None)
        future.cancel()
        raise exc

    future.set_result(result)

    if unless is None or not unless(result):
        cache[key] = result
    else:
        cache.futures.pop(key, None)

    return result

async def make_cache_key(args, kwargs, is_fastapi=False):
    """
    Cache key'ini oluşturur.
    
    :param is_fastapi (bool): Eğer True ise, ilk argümanın bir FastAPI Request nesnesi olduğu varsayılır.
        Bu durumda, cache key, request nesnesinin URL yolunu (request.url.path) ve 
        isteğe ait verilerden (GET istekleri için query parametreleri; diğer istekler için JSON veya form verileri)
        elde edilen verinin URL uyumlu halinin md5 hash'inin birleşiminden oluşturulur.
        Böylece, aynı URL ve aynı istek verileri için her seferinde aynı cache key üretilecektir.
        Eğer False ise, cache key args ve kwargs değerlerinden, sıralı bir tuple olarak oluşturulur.
    """
    if not is_fastapi:
        return (args, tuple(sorted(kwargs.items())))

    request = args[0] if args else kwargs.get("request")

    if request.method == "GET":
        veri = dict(request.query_params) if request.query_params else None
    else:
        try:
            veri = await request.json()
        except Exception:
            form_data = await request.form()
            veri = dict(form_data.items())

    args_hash = md5(urlencode(veri).encode()).hexdigest() if veri else ""
    return f"{request.url.path}?{args_hash}"


def kekik_cache(ttl=UNLIMITED, unless=None, is_fastapi=False):
    """
    Bir fonksiyon veya coroutine'in sonucunu cache'ler.
    
    :param ttl: Cache’in geçerlilik süresi (saniye). UNLIMITED ise süresizdir.
    :param unless: Fonksiyonun sonucunu argüman olarak alan bir callable. 
                   Eğer True dönerse, sonuç cache'e alınmaz.
    :param is_fastapi: Eğer True ise, cache key'i oluştururken FastAPI request nesnesine özel şekilde davranır.

    Örnek kullanım:
    
        @kekik_cache(ttl=15, unless=lambda res: res is None)
        async def bakalim(param):
            ...
    """
    # Parametresiz kullanıldığında
    if callable(ttl):
        return kekik_cache(UNLIMITED, unless=unless, is_fastapi=is_fastapi)(ttl)

    def decorator(func):
        func.__cache = AsyncCache(ttl)

        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                key = await make_cache_key(args, kwargs, is_fastapi)

                try:
                    return await func.__cache.get(key)
                except KeyError:
                    return await _async_compute_and_cache(func, key, unless, *args, **kwargs)

            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                key = (args, tuple(sorted(kwargs.items())))

                try:
                    return func.__cache[key]
                except KeyError:
                    result = func(*args, **kwargs)
                    _sync_maybe_cache(func, key, result, unless)
                    return result

            return sync_wrapper

    return decorator