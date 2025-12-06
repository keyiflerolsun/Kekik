# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

"""Cache Decorator"""

from __future__ import annotations
import asyncio
from functools import wraps
from typing import Any, Callable, TypeVar

from .backends import MemoryCache, AsyncMemoryCache, HybridCache, AsyncHybridCache
from .serializers import make_cache_key

F = TypeVar("F", bound=Callable[..., Any])


def kekik_cache(
    ttl: int | None = None,
    unless: Callable[[Any], bool] | None = None,
    use_redis: bool = True,
    max_size: int = 10000,
) -> Callable[[F], F]:
    """
    Fonksiyon sonuçlarını cache'leyen decorator.

    Args:
        ttl: Cache geçerlilik süresi (saniye). None = süresiz.
        unless: True dönerse sonuç cache'lenmez.
        use_redis: True = Redis + memory fallback, False = sadece memory.
        max_size: Maksimum cache boyutu (LRU eviction).

    Örnekler:
        >>> @kekik_cache(ttl=300)
        ... def hesapla(x, y):
        ...     return x + y

        >>> @kekik_cache(ttl=600, use_redis=False)
        ... async def veri_al(id):
        ...     return await db.fetch(id)

        >>> @kekik_cache(ttl=300, unless=lambda r: r.get("error"))
        ... async def api_call():
        ...     return {"data": "..."}
    """

    # Parametresiz kullanım: @kekik_cache
    if callable(ttl):
        func = ttl
        return kekik_cache(ttl=None, unless=unless, use_redis=use_redis, max_size=max_size)(func)

    def decorator(func: F) -> F:

        if asyncio.iscoroutinefunction(func):
            return _wrap_async(func, ttl, unless, use_redis, max_size)

        return _wrap_sync(func, ttl, unless, use_redis, max_size)

    return decorator


def _wrap_sync(
    func: Callable,
    ttl: int | None,
    unless: Callable | None,
    use_redis: bool,
    max_size: int,
) -> Callable:
    """Senkron fonksiyonu cache wrapper'ı ile sar."""

    cache = HybridCache(ttl, max_size) if use_redis else MemoryCache(ttl, max_size)
    func.__cache__ = cache

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = make_cache_key(func, args, kwargs)

        # Cache hit?
        try:
            return cache.get(key)
        except KeyError:
            pass

        # Cache miss - hesapla
        result = func(*args, **kwargs)

        # Unless kontrolü
        if unless is None or not unless(result):
            cache.set(key, result)

        return result

    return wrapper


def _wrap_async(
    func: Callable,
    ttl: int | None,
    unless: Callable | None,
    use_redis: bool,
    max_size: int,
) -> Callable:
    """Asenkron fonksiyonu cache wrapper'ı ile sar."""

    cache = AsyncHybridCache(ttl, max_size) if use_redis else AsyncMemoryCache(ttl, max_size)
    func.__cache__ = cache

    @wraps(func)
    async def wrapper(*args, **kwargs):
        key = make_cache_key(func, args, kwargs)

        # Cache hit?
        try:
            return await cache.get(key)
        except KeyError:
            pass

        # Eşzamanlı istek yönetimi
        if key in cache.futures:
            return await cache.futures[key]

        future = asyncio.Future()
        cache.futures[key] = future

        try:
            result = await func(*args, **kwargs)
            future.set_result(result)

            # Unless kontrolü
            if unless is None or not unless(result):
                await cache.set(key, result)

            return result

        except Exception as exc:
            future.cancel()
            raise exc

        finally:
            cache.futures.pop(key, None)

    return wrapper
