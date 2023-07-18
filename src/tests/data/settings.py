from src.backend.config import Settings

TEST_SETTINGS = Settings(
    API_VERSION="test",
    DEBUG=True,
    ENV="test",
    DB_HOST="test_redis",
    DB_PORT=1111,
    JWT_SECRET="111111111111",
)
