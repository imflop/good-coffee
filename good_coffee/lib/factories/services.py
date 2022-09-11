from logging import Logger

from fastapi import Depends

from ..clients.telegram import TelegramClient
from ..dal.coffeshops import CoffeeShopRepository
from ..services.telegram import TelegramService
from ..settings import AppSettings
from .base import loguru_factory, settings_factory
from .clients import telegram_client_factory
from .repositories import coffee_shop_repository_factory


def telegram_service_factory(
    client: TelegramClient = Depends(telegram_client_factory),
    settings: AppSettings = Depends(settings_factory),
    repository: CoffeeShopRepository = Depends(coffee_shop_repository_factory),
    logger: Logger = Depends(loguru_factory),
) -> TelegramService:
    return TelegramService(
        api_url=f"https://api.telegram.org/bot{settings.telegram_api_token}",
        client=client,
        repository=repository,
        logger=logger,
    )
