import logging
import uuid

from sqlalchemy import UniqueConstraint, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import expression
from werkzeug.security import check_password_hash, generate_password_hash

from flask_app.db import db


class BaseID(db.Model):
    __abstract__ = True

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )


class BaseCreate(db.Model):
    __abstract__ = True

    create_at = db.Column(db.DateTime, default=func.now(), nullable=False)


class ToDictMixin:
    def to_dict(self):
        data = self.__dict__
        out = dict()
        for key, value in data.items():
            if key == "_sa_instance_state" or value is None:
                continue
            out[key] = str(value)
        return out


class User(BaseID, BaseCreate, ToDictMixin):
    login = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(120), nullable=False)
    is_superuser = db.Column(db.Boolean, server_default=expression.false())
    histories = db.relationship("LoginHistory")
    roles = db.relationship(
        "Role", secondary="user_role_relation", backref="users"
    )

    def __repr__(self):
        return f"<User {self.login}>"

    def set_password(self, password=None):
        if password is None:
            password = self.password
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Role(BaseID, BaseCreate, ToDictMixin):
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(200), unique=True, nullable=True)
    permissions = db.relationship(
        "Permission", secondary="role_permission_relation", backref="roles"
    )

    def __repr__(self):
        return f"<Role {self.id}>"


class Permission(BaseID, BaseCreate, ToDictMixin):
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    model = db.Column(db.String(200), nullable=True)
    action = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"<Permission {self.id}>"


class UserRoleRelation(BaseID, BaseCreate, ToDictMixin):
    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("user.id"),
        nullable=False,
    )
    role_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("role.id"),
        nullable=False,
    )

    def __repr__(self):
        return f"<UserRoleRelation {self.id}>"


class RolePermissionRelation(BaseID, BaseCreate, ToDictMixin):
    role_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("role.id"),
        nullable=False,
    )
    permission_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("permission.id"),
        nullable=False,
    )

    def __repr__(self):
        return f"<RolePermissionRelation {self.id}>"


def create_login_history_partition(target, connection, **kw):
    """creating partition by login_history"""
    try:
        logging.info("Create partitions")
        connection.execute(
            text(
                """CREATE TABLE IF NOT EXISTS public.login_history_2022 
            PARTITION OF login_history FOR VALUES FROM 
            ('2022-01-01') TO ('2022-12-31');"""
            )
        )
        connection.execute(
            text(
                """CREATE TABLE IF NOT EXISTS public.login_history_2023 
            PARTITION OF login_history FOR VALUES FROM 
            ('2023-01-01') TO ('2023-12-31');"""
            )
        )
        logging.info("Finished creating partitions")
    except Exception as error:
        logging.info(
            "Did nor created partitions. Error: {error}".format(error=error)
        )


class LoginHistory(db.Model, ToDictMixin):
    __tablename__ = "login_history"
    __table_args__ = (
        UniqueConstraint("id", "create_at"),
        {
            "postgresql_partition_by": "RANGE (create_at)",
            "listeners": [("after_create", create_login_history_partition)],
        },
    )
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    create_at = db.Column(
        db.DateTime,
        primary_key=True,
        default=func.now(),
        nullable=False,
    )
    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("user.id"),
        nullable=False,
    )

    def __repr__(self):
        return f"<LoginHistory {self.id}>"
