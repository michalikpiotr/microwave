""" Redis DB operations"""
from src.backend.crud.base import DbCrud
from src.backend.services.db_connection import get_redis_db


class RedisCrud(DbCrud):
    """Redis db class"""

    def __init__(self):
        self._redis_client = get_redis_db()

    def get_item(self, item):
        return self._redis_client.get(item)

    def create_item(self, item, values):
        return self._redis_client.set(item, values)
