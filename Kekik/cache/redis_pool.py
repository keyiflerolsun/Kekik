# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

"""Redis Connection Pool Yönetimi - Singleton Pattern"""

from __future__ import annotations
import atexit
import threading
from typing import TYPE_CHECKING

import redis
import redis.asyncio as redis_async

if TYPE_CHECKING:
    from redis import ConnectionPool
    from redis.asyncio import ConnectionPool as AsyncConnectionPool

# -----------------------------------------------------
# Konfigürasyon
# -----------------------------------------------------
class RedisConfig:
    """Redis bağlantı ayarları."""
    HOST: str            = "127.0.0.1"
    PORT: int            = 6379
    DB: int              = 0
    PASSWORD: str | None = None
    MAX_CONNECTIONS: int = 50
    SOCKET_TIMEOUT: int  = 5
    HEALTH_CHECK: int    = 30


# -----------------------------------------------------
# Singleton Pool Manager
# -----------------------------------------------------
class RedisPoolManager:
    """
    Redis ConnectionPool yönetimi için singleton sınıf.
    Thread-safe ve lazy initialization destekler.
    """
    _instance: RedisPoolManager | None = None
    _lock = threading.Lock()

    def __new__(cls) -> RedisPoolManager:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init_pools()
        return cls._instance

    def _init_pools(self) -> None:
        """Pool değişkenlerini başlat."""
        self._sync_pool: ConnectionPool | None = None
        self._async_pool: AsyncConnectionPool | None = None
        self._async_initialized = False
        self._sync_pool_lock = threading.Lock()
        self._register_cleanup()

    def _get_pool_kwargs(self) -> dict:
        """Ortak pool parametrelerini döndür."""
        return {
            "host"                   : RedisConfig.HOST,
            "port"                   : RedisConfig.PORT,
            "db"                     : RedisConfig.DB,
            "password"               : RedisConfig.PASSWORD,
            "decode_responses"       : False,
            "max_connections"        : RedisConfig.MAX_CONNECTIONS,
            "socket_timeout"         : RedisConfig.SOCKET_TIMEOUT,
            "socket_connect_timeout" : RedisConfig.SOCKET_TIMEOUT,
            "retry_on_timeout"       : True,
            "health_check_interval"  : RedisConfig.HEALTH_CHECK,
        }

    # ----- Senkron Pool -----
    def get_sync_pool(self) -> ConnectionPool | None:
        """Senkron Redis pool döndür (lazy, thread-safe)."""
        if self._sync_pool is not None:
            return self._sync_pool

        with self._sync_pool_lock:
            if self._sync_pool is not None:
                return self._sync_pool

            try:
                self._sync_pool = redis.ConnectionPool(**self._get_pool_kwargs())
                # Bağlantı testi
                redis.Redis(connection_pool=self._sync_pool).ping()
                return self._sync_pool
            except Exception:
                self._sync_pool = None
                return None

    def get_sync_client(self) -> redis.Redis | None:
        """Senkron Redis client döndür."""
        pool = self.get_sync_pool()
        return redis.Redis(connection_pool=pool) if pool else None

    # ----- Asenkron Pool -----
    async def get_async_pool(self) -> AsyncConnectionPool | None:
        """Asenkron Redis pool döndür (lazy)."""
        if self._async_initialized:
            return self._async_pool

        try:
            self._async_pool = redis_async.ConnectionPool(**self._get_pool_kwargs())
            # Bağlantı testi
            client = redis_async.Redis(connection_pool=self._async_pool)
            await client.ping()
            await client.aclose()
            self._async_initialized = True
            return self._async_pool
        except Exception:
            self._async_pool = None
            self._async_initialized = True
            return None

    async def get_async_client(self) -> redis_async.Redis | None:
        """Asenkron Redis client döndür."""
        pool = await self.get_async_pool()
        return redis_async.Redis(connection_pool=pool) if pool else None

    # ----- Cleanup -----
    def _register_cleanup(self) -> None:
        """Program kapanışında pool'ları temizle."""
        atexit.register(self._cleanup)

    def _cleanup(self) -> None:
        """Pool'ları kapat."""
        if self._sync_pool:
            try:
                self._sync_pool.disconnect()
            except Exception:
                pass
            self._sync_pool = None

        if self._async_pool:
            try:
                # Async pool için internal bağlantıları temizle
                if hasattr(self._async_pool, '_available_connections'):
                    self._async_pool._available_connections.clear()
                if hasattr(self._async_pool, '_in_use_connections'):
                    self._async_pool._in_use_connections.clear()
            except Exception:
                pass
            self._async_pool = None
            self._async_initialized = False

    async def acleanup(self) -> None:
        """Pool'ları asenkron kapat."""
        if self._sync_pool:
            try:
                self._sync_pool.disconnect()
            except Exception:
                pass
            self._sync_pool = None

        if self._async_pool:
            try:
                await self._async_pool.disconnect()
            except Exception:
                pass
            self._async_pool = None
            self._async_initialized = False


# Global singleton instance
_pool_manager = RedisPoolManager()

# Convenience functions
def get_sync_redis() -> redis.Redis | None:
    """Senkron Redis client al."""
    return _pool_manager.get_sync_client()

async def get_async_redis() -> redis_async.Redis | None:
    """Asenkron Redis client al."""
    return await _pool_manager.get_async_client()

def close_pools() -> None:
    """Pool'ları kapat."""
    _pool_manager._cleanup()

async def aclose_pools() -> None:
    """Pool'ları asenkron kapat."""
    await _pool_manager.acleanup()
