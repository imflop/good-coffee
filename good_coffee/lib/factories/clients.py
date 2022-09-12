from logging import Logger

from fastapi import Depends

from ..clients.base import BaseHTTPClient
from ..clients.telegram import TelegramClient
from .base import loguru_factory


def telegram_client_factory(logger: Logger = Depends(loguru_factory)) -> TelegramClient:
    return TelegramClient(http_client=BaseHTTPClient(logger=logger), logger=logger)
