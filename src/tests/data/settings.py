from src.backend.config import Settings

TEST_SETTINGS = Settings(
    API_VERSION="test",
    DEBUG=True,
    ENV="test",
    DB_HOST="test_redis",
    DB_PORT=1111,
    JWT_SECRET="test_secret",
    DEFAULT_MICROWAVE_ID="test1",
    DEFAULT_MICROWAVE_MAX_POWER=2000,
    DEFAULT_MICROWAVE_MIN_POWER=0,
    DEFAULT_MICROWAVE_MAX_COUNTER=1000,
    DEFAULT_MICROWAVE_MIN_COUNTER=0,
    ADMIN_USER="Admin User 1",
)
