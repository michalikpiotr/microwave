""" Config values module"""
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings used in app"""

    API_NAME: str = "Microwave Oven API"
    API_VERSION: str
    JWT_SECRET: str
    DEBUG: bool
    ENV: str
    DB_HOST: str
    DB_PORT: int
    DB_TYPE: str = "redis"
    DEFAULT_MICROWAVE_ID_1: str = "microwave_1"
    DEFAULT_MICROWAVE_ID_2: str = "microwave_2"
    DEFAULT_MICROWAVE_MAX_POWER: int = 1500
    DEFAULT_MICROWAVE_MIN_POWER: int = 0
    DEFAULT_MICROWAVE_MAX_COUNTER: int = 900
    DEFAULT_MICROWAVE_MIN_COUNTER: int = 0
    ADMIN_USER: str = "Piotr Michalik"


@lru_cache
def get_settings() -> Settings:
    """Creates and returns settings instance."""

    return Settings()
