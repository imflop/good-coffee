import typing as t
from enum import Enum

from pydantic import BaseModel, validator


class WiredCityName(Enum):
    NICOSIA_MUNICIPALITY = "Nicosia Municipality"


class NormalCityName(str, Enum):
    NICOSIA = "Nicosia"


class Address(BaseModel):
    city: str | None
    country: str
    country_code: str
    municipality: str

    @validator("city", pre=True)
    def wired_city_names(cls, v: t.Any) -> str:
        if isinstance(v, str) and v in cls._wired_city_names():
            if v == WiredCityName.NICOSIA_MUNICIPALITY.value:
                return NormalCityName.NICOSIA

        return v

    @staticmethod
    def _wired_city_names() -> tuple:
        return tuple(wcn.value for wcn in WiredCityName)


class OSM(BaseModel):
    place_id: int
    licence: str
    osm_type: str
    osm_id: int
    lat: float
    lon: float
    display_name: str
    address: Address
