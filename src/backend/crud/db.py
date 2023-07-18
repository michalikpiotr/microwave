from src.backend.crud.redis import RedisCrud

factory = {
    "redis": RedisCrud,
}

db_client = factory["redis"]
