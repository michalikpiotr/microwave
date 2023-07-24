""" DB selector based on config"""
from src.backend.config import get_settings
from src.backend.crud.redis import RedisCrud


class DBFactory:
    """DB Factory"""

    _databases = {
        "redis": RedisCrud,
    }

    def __call__(self):
        return self._databases[get_settings().DB_TYPE]()


db_client = DBFactory()
