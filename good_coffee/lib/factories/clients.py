from logging import Logger

from fastapi import Depends

from ..clients.bases.geo_client import BaseGeocoderClient
from ..clients.bases.http_client import BaseHTTPClient
from ..clients.geocoder import GeocoderClient
from ..clients.telegram import TelegramClient
from .base import loguru_factory


def telegram_client_factory(logger: Logger = Depends(loguru_factory)) -> TelegramClient:
    return TelegramClient(http_client=BaseHTTPClient(logger=logger), logger=logger)


def geocoder_client_factory() -> GeocoderClient:
    return GeocoderClient(geo_client=BaseGeocoderClient())
