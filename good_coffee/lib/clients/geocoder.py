import dataclasses as dc

from ..deserializers.geocoder import OSM
from .bases.geo_client import BaseGeocoderClient, OSMGeocoderProto


@dc.dataclass(frozen=True, slots=True)
class GeocoderClient:
    geo_client: BaseGeocoderClient

    async def get_city(self, latitude: float, longitude: float) -> OSM:
        geocoder = await self._get_client()
        result = await geocoder.reverse((latitude, longitude), language="en")

        return OSM.parse_obj(result.raw)

    async def _get_client(self) -> OSMGeocoderProto:
        return await self.geo_client.get_client()
