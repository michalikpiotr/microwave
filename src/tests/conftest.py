""" Pytest global conftest """
from unittest.mock import patch

import pytest
from starlette.testclient import TestClient

from src.main import app
from src.tests.data.settings import TEST_SETTINGS


@pytest.fixture(scope="function", autouse=True)
def config_settings_mock(monkeypatch) -> None:
    """Sets application required environment variables with test settings."""

    for key, value in TEST_SETTINGS.model_dump().items():
        monkeypatch.setenv(key, str(value))


@pytest.fixture(scope="module")
def client():
    """Yields client app fixture to use within tests."""

    with patch("src.main.get_settings", return_value=TEST_SETTINGS):
        test_app = app()
        yield TestClient(test_app)
