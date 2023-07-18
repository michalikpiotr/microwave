import redis
from redis import Redis

from src.backend.config import get_settings


def get_redis_db() -> Redis:
    """Redis DB client"""

    settings = get_settings()

    redis_db = redis.Redis(host=settings.DB_HOST, port=settings.DB_PORT)

    try:
        return redis_db
    finally:
        redis_db.close()
