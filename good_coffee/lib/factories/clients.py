from logging import Logger

from fastapi import Depends

from ..clients.telegram import TelegramClient
from .base import loguru_factory


def telegram_client_factory(logger: Logger = Depends(loguru_factory)) -> TelegramClient:
    return TelegramClient(logger=logger)
