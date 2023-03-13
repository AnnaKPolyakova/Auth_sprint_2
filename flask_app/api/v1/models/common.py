import uuid

from pydantic import BaseModel


class IDAndConfigMixin(BaseModel):
    id: str


class CreateAtMixin(BaseModel):
    create_at: str


class Status(BaseModel):
    status: str


class ResultBool(BaseModel):
    result: bool


class UserId(BaseModel):
    id: uuid.UUID
