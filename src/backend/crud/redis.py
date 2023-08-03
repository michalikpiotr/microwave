""" Redis DB operations"""
import redis

from src.backend.config import get_settings
from src.backend.crud.base import DbCrud


class RedisCrud(DbCrud):
    """Redis Crud operations with context manager"""

    def __init__(self):
        self._db_client = None
        self.settings = get_settings()

    def get_item(self, item):
        """Get redis item details"""
        return self._db_client.get(item)

    def create_item(self, item, values):
        """Create redis item with values"""
        self._db_client.set(item, values)

    @property
    def db_client(self):
        """Get redis client"""
        return self._db_client

    @db_client.setter
    def db_client(self, client):
        """Set redis client direct or transaction communication"""
        self._db_client = client

    def __enter__(self):
        self._db_client = redis.Redis(
            host=self.settings.DB_HOST, port=self.settings.DB_PORT
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._db_client is not None:
            self._db_client.close()


class RedisTransaction(RedisCrud):
    """Redis Transaction operations with context manager"""

    def __init__(self, db_connection):
        super().__init__()
        self.db_connection = db_connection

    def __enter__(self):
        self.db_client = self.db_connection.db_client.pipeline()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.db_client.execute()
        except redis.exceptions.RedisError:
            self.db_client.reset()
