import dataclasses as dc

from ..deserializers.geocoder import OSM
from .bases.geo_client import BaseGeocoderClient


@dc.dataclass(frozen=True, slots=True)
class GeocoderClient:
    geo_client: BaseGeocoderClient

    async def get_city(self, latitude: float, longitude: float) -> OSM:
        geocoder = await self.geo_client.get_geocoder()
        result = await geocoder.reverse((latitude, longitude), language="en")

        return OSM.parse_obj(result.raw)
