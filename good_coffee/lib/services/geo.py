import dataclasses as dc
import typing as t
from math import asin, cos, radians, sin, sqrt

from ..dal.models.coffeeshops import CoffeeShopModel


class DistanceToCoffeeShop(t.NamedTuple):
    distance: float
    CoffeeShop: CoffeeShopModel


@dc.dataclass(frozen=True, slots=True)
class GeoService:
    # The "Earth radius" R varies from 6356.752 km at the poles to 6378.137 km at the equator.
    earth_radius: int = dc.field(default=6378)

    def find_closest(self, coffee_shops: list[CoffeeShopModel], lat: float, long: float) -> list[t.Any]:
        return self._find_closest_by_coordinates(coffee_shops, lat, long)

    def _find_closest_by_coordinates(
        self, coffee_shops: t.Sequence[CoffeeShopModel], source_latitude: float, source_longitude: float
    ) -> list[t.Any]:
        result: list[DistanceToCoffeeShop] = [
            DistanceToCoffeeShop(
                self._distance_between_two_coordinates(
                    coffee_shop.latitude, coffee_shop.longitude, source_longitude, source_latitude
                ),
                coffee_shop,
            )
            for coffee_shop in coffee_shops
        ]

        return sorted(result, key=lambda x: x.distance)

    def _distance_between_two_coordinates(
        self, cs_latitude: float, cs_longitude: float, s_latitude: float, s_longitude: float
    ) -> float:
        cs_lat, cs_long, s_lat, s_long = map(radians, [cs_latitude, cs_longitude, s_latitude, s_longitude])

        dist_lats = abs(cs_lat - s_lat)
        dist_longs = abs(cs_long - s_long)
        a = sin(dist_lats / 2) ** 2 + cos(cs_lat) * cos(s_lat) * sin(dist_longs / 2) ** 2
        c = asin(sqrt(a)) * 2

        return c * self.earth_radius
