from __future__ import annotations

import dataclasses as dc
import logging
import typing as t
from enum import Enum
from logging import Logger

from ..clients.telegram import TelegramClient
from ..dal.coffeshops import CoffeeShopRepository
from ..serializers.keyboard import Button, Keyboard
from ..serializers.telegram import Message

logger = logging.getLogger(__name__)


class TelegramMethods(str, Enum):
    SEND_MESSAGE = "sendMessage"


@dc.dataclass(frozen=True, slots=True)
class TelegramService:
    api_url: str
    client: TelegramClient
    repository: CoffeeShopRepository
    logger: Logger = dc.field(default=logging.getLogger(__name__))

    async def get_coffee_shop(self, coffee_shop_id: int) -> str:
        shop = await self.repository.get(coffee_shop_id)

        return shop.name if shop else None

    async def process_message(self, message: Message) -> None:
        if message.text == "/start":
            await self.send_welcome_message(message.chat.id)
        else:
            self.logger.info("Unknown command")

    async def send_welcome_message(self, chat_id: int) -> None:
        keyboard = Keyboard(keyboard=[[Button(text="📍Current location", request_location=True)]])
        data_to_sent = self._construct_sending_object(
            chat_id=chat_id, message="Hello there, send me your location", keyboard=keyboard
        )
        await self._send_message(data_to_sent)

    async def _send_message(self, sending_data: t.Mapping[str, t.Any]) -> None:
        # TODO: add retrie
        result = await self.client.post(url=f"{self.api_url}/{TelegramMethods.SEND_MESSAGE}", data=sending_data)

        self.logger.debug(result)

    @staticmethod
    def _construct_sending_object(chat_id: int, message: str, keyboard: Keyboard | None) -> t.Mapping[str, t.Any]:
        return {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "html",
            "reply_markup": keyboard.json() if keyboard else None,
        }
