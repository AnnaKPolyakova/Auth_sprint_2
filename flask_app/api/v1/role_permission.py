import logging
from http import HTTPStatus
from typing import List

from flask import Blueprint, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from spectree import Response

from flask_app.api.v1.models.common import Status
from flask_app.api.v1.models.permission import (
    Permission,
    RolePermission,
    RolePermissionCreate,
)
from flask_app.api.v1.utils.other import doc, superuser_only
from flask_app.api.v1.utils.managers import dell_obj
from flask_app.api.v1.utils.role_permission import (
    RolePermissionCreator,
    get_role_permissions,
)

from flask_app.db import db
from flask_app.db_models import Permission as Permission_db_model
from flask_app.db_models import Role as Role_db_model
from flask_app.db_models import (
    RolePermissionRelation as RolePermissionRelation_db_model,
)

role_permissions = Blueprint("role_permissions", __name__)


class RolePermissionsAPI(MethodView):
    @jwt_required(verify_type=False)
    @doc.validate(
        tags=["role_permissions"],
        resp=Response(
            HTTP_200=(List[Permission], "Get all permissions for role"),
            HTTP_404=("", "Object does not exist"),
        ),
    )
    def get(self, role_id):
        logging.debug(f"RolePermissionsAPI {self.get.__name__} start")
        role = db.session.get(Role_db_model, role_id)
        if role is None:
            logging.info(f"RolePermissionsAPI {self.get.__name__} NOT_FOUND")
            return "", HTTPStatus.NOT_FOUND
        permissions = get_role_permissions(role)
        logging.debug(f"RolePermissionsAPI {self.get.__name__} end")
        return [
            Permission(
                **permission.to_dict()
            ).dict() for permission in permissions
        ], HTTPStatus.OK

    @jwt_required(verify_type=False)
    @superuser_only
    @doc.validate(
        tags=["role_permissions"],
        json=RolePermissionCreate,
        resp=Response(
            HTTP_201=(RolePermission, "Add role to user"),
            HTTP_403=(Status, "Superuser only"),
            HTTP_404=("", "Object does not exist"),
        ),
    )
    def post(self, role_id):
        logging.debug(f"RolePermissionsAPI {self.post.__name__} start")
        role = db.session.get(Role_db_model, role_id)
        permission_id = request.get_json()["permission_id"]
        permission = db.session.get(Permission_db_model, permission_id)
        if role is None or permission is None:
            logging.info(f"RolePermissionsAPI {self.post.__name__} NOT_FOUND")
            return "", HTTPStatus.NOT_FOUND
        if (
            RolePermissionRelation_db_model.query.filter_by(
                role_id=role_id, permission_id=permission_id
            ).count()
            > 0
        ):
            logging.info(
                f"RolePermissionsAPI {self.post.__name__} BAD_REQUEST"
            )
            return {
                "status": "User already have this role"
            }, HTTPStatus.BAD_REQUEST
        creator = RolePermissionCreator(
            {"role_id": role_id, "permission_id": permission_id},
            RolePermission,
            RolePermissionRelation_db_model,
            db,
        )
        result, info = creator.save()
        if result is False:
            logging.info(
                f"RolePermissionsAPI {self.post.__name__} BAD_REQUEST"
            )
            return {"status": {info}}, HTTPStatus.BAD_REQUEST
        logging.debug(f"RolePermissionsAPI {self.post.__name__} end")
        return info, HTTPStatus.CREATED


class RolePermissionsDetailAPI(MethodView):
    @jwt_required(verify_type=False)
    @superuser_only
    @doc.validate(
        tags=["role_permissions"],
        resp=Response(
            HTTP_200=(Status, "Permission were delete for role"),
            HTTP_404=("", "Permission does not exist for role"),
            HTTP_403=(Status, "Superuser only"),
        ),
    )
    def delete(self, role_id, permission_id):
        logging.debug(f"RolePermissionsDetailAPI {self.delete.__name__} start")
        user_role = RolePermissionRelation_db_model.query.filter_by(
            role_id=role_id, permission_id=permission_id
        ).first()
        if user_role is None:
            return "", HTTPStatus.NOT_FOUND
        result, info = dell_obj(db, [user_role])
        if result is False:
            logging.info(
                f"RolePermissionsDetailAPI {self.delete.__name__} BAD_REQUEST"
            )
            return {"status": info}, HTTPStatus.BAD_REQUEST
        logging.debug(f"RolePermissionsDetailAPI {self.delete.__name__} end")
        return {"status": "success"}, HTTPStatus.OK


role_permissions.add_url_rule(
    "/", view_func=RolePermissionsAPI.as_view("role_permissions")
)
role_permissions.add_url_rule(
    "/<path:permission_id>/",
    view_func=RolePermissionsDetailAPI.as_view("role_permissions_detail"),
)
