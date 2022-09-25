import logging
import typing as t
from logging import Logger

from fastapi import APIRouter, Depends, Request, Response, status

from ...lib.dal.coffeshops import CoffeeShopRepository
from ...lib.factories.base import loguru_factory
from ...lib.factories.repositories import coffee_shop_repository_factory
from ...lib.factories.services import (geo_service_factory,
                                       telegram_service_factory)
from ...lib.serializers.telegram import HookResponse
from ...lib.services.geo import GeoService
from ...lib.services.telegram import TelegramService

router = APIRouter()


@router.get("/debug-q", status_code=status.HTTP_200_OK)
async def get_coffee_shop(
    request: Request,
    coffee_shop_id: int,
    service: TelegramService = Depends(telegram_service_factory),
    logger: Logger = Depends(loguru_factory),
) -> str:
    logger.info(f"Received request from: {request.client.host if request.client else None}")

    return await service.get_coffee_shop(coffee_shop_id=coffee_shop_id)


@router.get("/debug-coords", status_code=status.HTTP_200_OK)
async def get_city_name(
    lat: float,
    long: float,
    service: TelegramService = Depends(telegram_service_factory),
    repos: CoffeeShopRepository = Depends(coffee_shop_repository_factory),
    geo_service: GeoService = Depends(geo_service_factory),
    logger: Logger = Depends(loguru_factory),
) -> t.Any:
    logger.info(f"Received latitude: {lat} longitude: {long}")

    city_name = await service.get_city(lat, long)
    shops = await repos.get_coffee_shops(city_name)
    closest = geo_service.find_closest(shops, lat, long)
    return closest


@router.post("/telegram", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def location(
    request: Request,
    hook: HookResponse,
    service: TelegramService = Depends(telegram_service_factory),
    logger: logging.Logger = Depends(loguru_factory),
) -> None:
    # hook_json = await request.json()
    # hook = HookResponse.parse_obj(hook_json)
    logger.info(f"Received hook response from: {request.client.host if request.client else None}")

    await service.process_message(hook.message)
