# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

"""
Kekik Cache Module

Senkron ve asenkron fonksiyonlar için cache desteği.
Redis + in-memory hybrid cache veya sadece in-memory cache kullanılabilir.

Kullanım:
    >>> from Kekik.cache import kekik_cache
    >>>
    >>> @kekik_cache(ttl=300)
    ... def hesapla(x, y):
    ...     return x + y
    >>>
    >>> @kekik_cache(ttl=600, use_redis=False)
    ... async def veri_al(id):
    ...     return await db.fetch(id)
"""

from .decorator import kekik_cache
from .backends import MemoryCache, AsyncMemoryCache, HybridCache, AsyncHybridCache
from .redis_pool import (
    RedisConfig,
    get_sync_redis,
    get_async_redis,
    close_pools,
    aclose_pools,
)
from .serializers import serialize, deserialize, make_cache_key
