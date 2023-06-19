from typing import Optional

from pydantic import BaseModel

from flask_app.api.v1.models.common import CreateAtMixin, IDAndConfigMixin


class User(IDAndConfigMixin, CreateAtMixin):
    login: str
    email: Optional[str] = None
    is_superuser: bool


class UserCreate(BaseModel):
    login: str
    email: Optional[str] = None
    password: str


class UserUpdate(BaseModel):
    login: Optional[str]
    email: Optional[str]
    password: Optional[str]


class UserLogin(BaseModel):
    login: str
    password: str


class Tokens(BaseModel):
    access: str
    refresh: str


class AccessTokens(BaseModel):
    access: str


class UserId(BaseModel):
    user_id: str


class UserIds(BaseModel):
    ids: list
