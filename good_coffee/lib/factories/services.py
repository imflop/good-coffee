from logging import Logger

from fastapi import Depends

from ..clients.geocoder import GeocoderClient
from ..clients.telegram import TelegramClient
from ..dal.coffeshops import CoffeeShopRepository
from ..services.geo import GeoService
from ..services.telegram import TelegramService
from ..settings import AppSettings
from .base import loguru_factory, settings_factory
from .clients import geocoder_client_factory, telegram_client_factory
from .repositories import coffee_shop_repository_factory


def geo_service_factory() -> GeoService:
    return GeoService()


def telegram_service_factory(
    client: TelegramClient = Depends(telegram_client_factory),
    geocoder: GeocoderClient = Depends(geocoder_client_factory),
    geo_service: GeoService = Depends(geo_service_factory),
    settings: AppSettings = Depends(settings_factory),
    repository: CoffeeShopRepository = Depends(coffee_shop_repository_factory),
    logger: Logger = Depends(loguru_factory),
) -> TelegramService:
    return TelegramService(
        api_url=f"https://api.telegram.org/bot{settings.telegram_api_token}",
        client=client,
        geocoder=geocoder,
        geo_service=geo_service,
        repository=repository,
        logger=logger,
    )
