import dataclasses as dc
import typing as t
from math import asin, cos, radians, sin, sqrt

from ..dal.models.coffeeshops import CoffeeShopModel


@dc.dataclass(frozen=True, slots=True)
class GeoService:
    # The "Earth radius" R varies from 6356.752 km at the poles to 6378.137 km at the equator.
    earth_radius: int = dc.field(default=6378)

    def find_closest(self, coffee_shops: list[CoffeeShopModel], lat: float, long: float) -> list[t.Any]:
        data = self._find_closest_by_coords(coffee_shops, lat, long)
        return data

    def _distance_between_two_coords(self, *args):
        lat1, lat2, long1, long2 = map(radians, args)

        dist_lats = abs(lat2 - lat1)
        dist_longs = abs(long2 - long1)
        a = sin(dist_lats / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dist_longs / 2) ** 2
        c = asin(sqrt(a)) * 2

        return c * self.earth_radius

    def _find_closest_by_coords(
        self, coffee_shops: t.Sequence[CoffeeShopModel], source_latitude: float, source_longitude: float
    ) -> list[t.Any]:
        return min(
            coffee_shops,
            key=lambda x: self._distance_between_two_coords(source_latitude, x.latitude, source_longitude, x.longitude),
        )
