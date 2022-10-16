import pytest

from good_coffee.lib.settings import AppSettings
from good_coffee.lib.setup_app import setup_app


@pytest.fixture
def settings():
    return AppSettings(telegram_api_token="token", secret_key="secret-key")


@pytest.fixture
def app(settings):
    return setup_app(settings)
