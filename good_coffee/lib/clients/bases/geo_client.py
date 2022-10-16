from __future__ import annotations

import dataclasses as dc
import typing as t

import httpx
from geopy.adapters import BaseAsyncAdapter, _normalize_proxies
from geopy.geocoders import Nominatim
from geopy.geocoders.base import DEFAULT_SENTINEL

from .... import __module_name__, __version__


class OSMGeocoderProto(t.Protocol):
    def reverse(
        self,
        query: str | tuple,
        *,
        exactly_one: bool = True,
        timeout: int = DEFAULT_SENTINEL,
        language: bool | str = False,
        addressdetails: bool = True,
        zoom: int | None = None,
    ) -> t.Any:
        ...


class HttpxAsyncAdapter(BaseAsyncAdapter):
    def __init__(self, *, proxies, ssl_context):
        proxies = _normalize_proxies(proxies)
        super().__init__(proxies=proxies, ssl_context=ssl_context)

        self.proxies = proxies
        self.ssl_context = ssl_context

    async def get_text(self, url, *, timeout, headers) -> str:
        response = await self._request(url=url, timeout=timeout, headers=headers)
        response.raise_for_status()

        return response.text

    async def get_json(self, url, *, timeout, headers) -> t.Mapping[str, t.Any]:
        response = await self._request(url=url, timeout=timeout, headers=headers)
        response.raise_for_status()

        return response.json()

    @staticmethod
    async def _request(*, url, timeout, headers) -> httpx.Response:
        async with httpx.AsyncClient(headers=headers, timeout=timeout, trust_env=False) as client:
            return await client.request(method="GET", url=url)


@dc.dataclass(frozen=True, slots=True)
class BaseGeocoderClient:
    """
    Base geocoder client over geopy library
    """

    async def get_geocoder(self) -> OSMGeocoderProto:
        async with Nominatim(user_agent=self._get_user_agent(), adapter_factory=HttpxAsyncAdapter) as geocoder:
            return geocoder

    @staticmethod
    def _get_user_agent() -> str:
        return f"{__module_name__}/{__version__}"
