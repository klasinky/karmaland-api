from functools import lru_cache

from config.env import get_settings
from redis_client.connection import RedisConnection

settings = get_settings()


@lru_cache()
def get_redis():
    redis = RedisConnection(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0,
        password=settings.REDIS_PASSWORD
    )
    redis.connect()
    return redis
