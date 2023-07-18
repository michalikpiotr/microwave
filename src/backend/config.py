from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_NAME: str = "Microwave Oven API"
    API_VERSION: str
    JWT_SECRET: str
    DEBUG: bool
    ENV: str
    DB_HOST: str
    DB_PORT: int


@lru_cache
def get_settings() -> Settings:
    """Creates and returns settings instance."""

    return Settings()
