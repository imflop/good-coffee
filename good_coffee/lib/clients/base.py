from __future__ import annotations

import dataclasses as dc
import logging
import typing as t
from enum import Enum
from logging import Logger

import httpx


class Methods(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


@dc.dataclass(frozen=True, slots=True)
class BaseClient:
    """
    Base client
    """

    logger: Logger = dc.field(default=logging.getLogger(__name__))

    default_timeout: float = 35.0
    max_keepalive_connections: int = 5
    max_connections: int = 10

    async def request(
        self,
        url: str,
        method: str = Methods.GET,
        params: t.Mapping[str, t.Any] | None = None,
        json: t.Mapping[str, t.Any] | None = None,
        data: t.Mapping[str, t.Any] | None = None,
    ) -> httpx.Response:
        async with httpx.AsyncClient(
            limits=self._get_limits(),
            headers=self._get_headers(),
            timeout=self.default_timeout,
            event_hooks={
                "request": [self._log_request],
                "response": [self._log_response],
            },
        ) as client:
            return await client.request(
                method=method,
                url=url,
                params=params,
                json=json,
                data=data,
            )

    async def _log_request(self, request: httpx.Request) -> None:
        self.logger.debug(f"Request event hook: {request.method} {request.url} >> Waiting for response")

    async def _log_response(self, response: httpx.Response) -> None:
        request = response.request
        self.logger.debug(f"Response event hook: {request.method} {request.url} >> Status {response.status_code}")

    @staticmethod
    def _get_headers() -> httpx.Headers:
        return httpx.Headers({"Accept": "application/json"})

    def _get_limits(self) -> httpx.Limits:
        return httpx.Limits(
            max_keepalive_connections=self.max_keepalive_connections,
            max_connections=self.max_connections,
        )
