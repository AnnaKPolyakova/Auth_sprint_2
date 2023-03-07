from pydantic import BaseModel

from flask_app.api.v1.models.common import CreateAtMixin, IDAndConfigMixin


class Role(IDAndConfigMixin, CreateAtMixin):
    name: str
    description: str


class RoleCreate(BaseModel):
    name: str
    description: str


class UserRole(IDAndConfigMixin, CreateAtMixin):
    user_id: str
    role_id: str


class UserRoleCreate(BaseModel):
    role_id: str
