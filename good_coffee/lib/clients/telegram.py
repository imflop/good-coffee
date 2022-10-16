import dataclasses as dc
import logging
import typing as t
from logging import Logger

from .bases.http_client import BaseHTTPClient, Methods


@dc.dataclass(frozen=True, slots=True)
class TelegramClient:
    http_client: BaseHTTPClient
    logger: Logger = dc.field(default=logging.getLogger(__name__))

    async def post(self, url: str, data: t.Mapping[str, t.Any]) -> t.Mapping[str, t.Any]:
        response = await self.http_client.request(url=url, method=Methods.POST, data=data)

        try:
            return response.json()
        except Exception as e:
            self.logger.error(f"Error while parsing response: {e}")
            return {}
