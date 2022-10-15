import logging

from fastapi import APIRouter, Depends, Request, Response, status

from ...lib.factories.base import loguru_factory
from ...lib.factories.services import telegram_service_factory
from ...lib.serializers.telegram import HookResponse
from ...lib.services.telegram import TelegramService

router = APIRouter()


@router.post("/telegram", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def location(
    request: Request,
    hook: HookResponse,
    service: TelegramService = Depends(telegram_service_factory),
    logger: logging.Logger = Depends(loguru_factory),
) -> None:
    logger.info(f"Received hook response from: {request.client.host if request.client else None}")

    await service.process_message(hook.message)
