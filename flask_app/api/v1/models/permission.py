from typing import Optional

from pydantic import BaseModel

from flask_app.api.v1.models.common import CreateAtMixin, IDAndConfigMixin


class Permission(IDAndConfigMixin, CreateAtMixin):
    name: str
    description: Optional[str] = None
    model: Optional[str] = None
    action: Optional[str] = None


class PermissionCreate(BaseModel):
    name: str
    description: Optional[str] = None
    model: Optional[str] = None
    action: Optional[str] = None


class RolePermission(IDAndConfigMixin, CreateAtMixin):
    permission_id: str
    role_id: str


class RolePermissionCreate(BaseModel):
    permission_id: str


class CheckPermission(BaseModel):
    permission_id: str


class Page(BaseModel):
    page: Optional[int] = 1
