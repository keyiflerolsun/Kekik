# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

"""Cache Backend Sınıfları - In-Memory ve Hybrid"""

from __future__ import annotations
import asyncio
import threading
import time
from abc import ABC, abstractmethod
from typing import Any

from .redis_pool import get_sync_redis, get_async_redis
from .serializers import serialize, deserialize


# -----------------------------------------------------
# Base Cache Interface
# -----------------------------------------------------
class BaseCache(ABC):
    """Cache interface - tüm cache implementasyonları bu sınıftan türer."""

    @abstractmethod
    def get(self, key: str) -> Any:
        """Cache'ten değer al."""
        ...

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """Cache'e değer yaz."""
        ...


# -----------------------------------------------------
# In-Memory Cache (LRU + TTL)
# -----------------------------------------------------
class MemoryCache(BaseCache):
    """
    Thread-safe in-memory cache.
    TTL ve LRU eviction destekler.
    """

    def __init__(self, ttl: int | None = None, max_size: int = 10000):
        self._ttl      = ttl
        self._max_size = max_size
        self._data: dict[str, Any]   = {}
        self._times: dict[str, float] = {}
        self._access: dict[str, int]  = {}
        self._lock = threading.RLock()

        # Cleanup thread
        if ttl:
            self._start_cleanup_thread(min(ttl, 3600))

    def _start_cleanup_thread(self, interval: int) -> None:
        """Arka plan temizlik thread'i başlat."""
        def cleanup_loop():
            while True:
                time.sleep(interval)
                self._cleanup_expired()

        thread = threading.Thread(target=cleanup_loop, daemon=True)
        thread.start()

    def _cleanup_expired(self) -> None:
        """Süresi dolmuş entry'leri temizle."""
        with self._lock:
            for key in list(self._data.keys()):
                if self._is_expired(key):
                    self._remove(key)

    def _is_expired(self, key: str) -> bool:
        """Key'in süresinin dolup dolmadığını kontrol et."""
        if self._ttl is None:
            return False
        timestamp = self._times.get(key)
        return timestamp is not None and (time.time() - timestamp > self._ttl)

    def _remove(self, key: str) -> None:
        """Key'i cache'ten sil."""
        self._data.pop(key, None)
        self._times.pop(key, None)
        self._access.pop(key, None)

    def _evict_lru(self) -> None:
        """En az kullanılan entry'yi sil (LRU)."""
        if self._access:
            lru_key = min(self._access, key=self._access.get)
            self._remove(lru_key)

    def get(self, key: str) -> Any:
        with self._lock:
            if self._is_expired(key):
                self._remove(key)
                raise KeyError(key)

            if key not in self._data:
                raise KeyError(key)

            self._access[key] = self._access.get(key, 0) + 1
            return self._data[key]

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            # Kapasite kontrolü
            if len(self._data) >= self._max_size and key not in self._data:
                self._evict_lru()

            self._data[key]   = value
            self._access[key] = 0
            if self._ttl:
                self._times[key] = time.time()

    def __getitem__(self, key: str) -> Any:
        return self.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.set(key, value)


# -----------------------------------------------------
# Async Memory Cache
# -----------------------------------------------------
class AsyncMemoryCache(BaseCache):
    """
    Asenkron in-memory cache.
    TTL ve LRU eviction destekler.
    """

    def __init__(self, ttl: int | None = None, max_size: int = 10000):
        self._ttl      = ttl
        self._max_size = max_size
        self._data: dict[str, Any]   = {}
        self._times: dict[str, float] = {}
        self._access: dict[str, int]  = {}
        self.futures: dict[str, asyncio.Future] = {}
        self._cleanup_task: asyncio.Task | None = None

    def _ensure_cleanup(self) -> None:
        """Cleanup task'in çalıştığından emin ol."""
        if self._cleanup_task is None and self._ttl:
            try:
                loop = asyncio.get_running_loop()
                self._cleanup_task = loop.create_task(self._cleanup_loop())
            except RuntimeError:
                pass

    async def _cleanup_loop(self) -> None:
        """Periyodik temizlik döngüsü."""
        interval = min(self._ttl, 3600) if self._ttl else 3600
        while True:
            await asyncio.sleep(interval)
            self._cleanup_expired()

    def _cleanup_expired(self) -> None:
        """Süresi dolmuş entry'leri temizle."""
        for key in list(self._data.keys()):
            if self._is_expired(key):
                self._remove(key)

    def _is_expired(self, key: str) -> bool:
        """Key'in süresinin dolup dolmadığını kontrol et."""
        if self._ttl is None:
            return False
        timestamp = self._times.get(key)
        return timestamp is not None and (time.time() - timestamp > self._ttl)

    def _remove(self, key: str) -> None:
        """Key'i cache'ten sil."""
        self._data.pop(key, None)
        self._times.pop(key, None)
        self._access.pop(key, None)
        self.futures.pop(key, None)

    def _evict_lru(self) -> None:
        """En az kullanılan entry'yi sil."""
        if self._access:
            lru_key = min(self._access, key=self._access.get)
            self._remove(lru_key)

    async def get(self, key: str) -> Any:
        self._ensure_cleanup()

        if self._is_expired(key):
            self._remove(key)

        if key in self._data:
            self._access[key] = self._access.get(key, 0) + 1
            return self._data[key]

        # Aynı key için bekleyen future varsa onu bekle
        if key in self.futures and not self.futures[key].done():
            try:
                return await self.futures[key]
            except asyncio.CancelledError:
                pass

        raise KeyError(key)

    async def set(self, key: str, value: Any) -> None:
        self._ensure_cleanup()

        # Kapasite kontrolü
        if len(self._data) >= self._max_size and key not in self._data:
            self._evict_lru()

        self._data[key]   = value
        self._access[key] = 0
        if self._ttl:
            self._times[key] = time.time()


# -----------------------------------------------------
# Hybrid Cache (Redis + Memory Fallback)
# -----------------------------------------------------
class HybridCache(BaseCache):
    """
    Senkron hybrid cache.
    Önce Redis'e yazar/okur, hata durumunda memory cache kullanır.
    """

    def __init__(self, ttl: int | None = None, max_size: int = 10000):
        self._ttl = ttl
        self._memory = MemoryCache(ttl, max_size)
        self._redis_available: bool | None = None

    def _get_redis(self):
        """Redis client al, availability'yi cache'le."""
        if self._redis_available is False:
            return None

        client = get_sync_redis()
        if self._redis_available is None:
            self._redis_available = client is not None

        return client

    def get(self, key: str) -> Any:
        redis = self._get_redis()

        if redis:
            try:
                data = redis.get(key)
                if data is not None:
                    return deserialize(data)
            except Exception:
                pass

        # Fallback to memory
        return self._memory.get(key)

    def set(self, key: str, value: Any) -> None:
        redis = self._get_redis()

        if redis:
            try:
                serialized = serialize(value)
                if self._ttl:
                    redis.set(key, serialized, ex=self._ttl)
                else:
                    redis.set(key, serialized)
                return
            except Exception:
                pass

        # Fallback to memory
        self._memory.set(key, value)

    def __getitem__(self, key: str) -> Any:
        return self.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.set(key, value)


# -----------------------------------------------------
# Async Hybrid Cache
# -----------------------------------------------------
class AsyncHybridCache(BaseCache):
    """
    Asenkron hybrid cache.
    Önce Redis'e yazar/okur, hata durumunda memory cache kullanır.
    """

    def __init__(self, ttl: int | None = None, max_size: int = 10000):
        self._ttl = ttl
        self._memory = AsyncMemoryCache(ttl, max_size)
        self._redis_available: bool | None = None
        self._redis_client = None
        self.futures = self._memory.futures  # Decorator için

    async def _get_redis(self):
        """Redis client al, availability'yi cache'le."""
        if self._redis_available is False:
            return None

        if self._redis_client is None:
            self._redis_client = await get_async_redis()
            self._redis_available = self._redis_client is not None

        return self._redis_client

    async def get(self, key: str) -> Any:
        # Eşzamanlı istek kontrolü
        if key in self.futures and not self.futures[key].done():
            return await self.futures[key]

        redis = await self._get_redis()

        if redis:
            try:
                data = await redis.get(key)
                if data is not None:
                    return deserialize(data)
            except Exception:
                pass

        # Fallback to memory
        return await self._memory.get(key)

    async def set(self, key: str, value: Any) -> None:
        redis = await self._get_redis()

        if redis:
            try:
                serialized = serialize(value)
                if self._ttl:
                    await redis.set(key, serialized, ex=self._ttl)
                else:
                    await redis.set(key, serialized)
                return
            except Exception:
                pass

        # Fallback to memory
        await self._memory.set(key, value)
