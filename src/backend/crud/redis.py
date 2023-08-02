""" Redis DB operations"""
import redis

from src.backend.crud.base import DbCrud
from src.backend.services.db_connection import get_redis_db


class RedisCrud(DbCrud):
    """Redis db class"""

    def __init__(self):
        self._redis_client = get_redis_db()
        self._pipeline = self._redis_client.pipeline(transaction=True)

    def get_item(self, item):
        return self._redis_client.get(item)

    def create_item(self, item, values):
        self._pipeline.set(item, values)

    def execute_transaction(self):
        try:
            return self._pipeline.execute()
        except redis.exceptions.RedisError:
            self._pipeline.reset()
