from __future__ import annotations

import typing as t

from pydantic import BaseModel


class Common(BaseModel):
    id: int
    first_name: str | None
    last_name: str | None
    username: str


class From(Common):
    is_bot: bool
    language_code: str


class Chat(Common):
    type: str


class Location(BaseModel):
    latitude: float
    longitude: float


class Entities(BaseModel):
    offset: int
    length: int
    type: str


class Message(BaseModel):
    message_id: int
    message_from: From
    chat: Chat
    date: int
    text: str | None
    location: Location | None
    entities: t.Sequence[Entities] | None

    class Config:
        fields = {"message_from": "from"}


class HookResponse(BaseModel):
    update_id: int
    message: Message
