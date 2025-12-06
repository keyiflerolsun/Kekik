# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

"""
Geriye Dönük Uyumluluk İçin Cache Modülü

Yeni modüler yapı için: from Kekik.cache import kekik_cache
"""

# Yeni modüler yapıdan import
from .cache import kekik_cache, RedisConfig

# Redis config eski değişkenler
REDIS_HOST = RedisConfig.HOST
REDIS_PORT = RedisConfig.PORT
REDIS_DB   = RedisConfig.DB
REDIS_PASS = RedisConfig.PASSWORD
