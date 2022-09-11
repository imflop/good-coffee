import orjson
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode()


class Button(BaseModel):
    text: str
    request_location: bool = Field(default=False)

    class Config:
        json_dumps = orjson_dumps


class Keyboard(BaseModel):
    keyboard: list[list[Button]]
    one_time_keyboard: bool = Field(default=True)
    resize_keyboard: bool = Field(default=True)

    class Config:
        json_dumps = orjson_dumps
