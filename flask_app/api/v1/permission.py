import logging
from http import HTTPStatus
from typing import List

from flask import Blueprint, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from spectree import Response

from flask_app.api.v1.models.common import Status
from flask_app.api.v1.models.permission import Permission, PermissionCreate
from flask_app.api.v1.utils.managers import dell_obj
from flask_app.api.v1.utils.other import doc, superuser_only
from flask_app.api.v1.utils.permission import (
    PermissionCreator,
    PermissionUpdater,
    get_permissions,
)
from flask_app.db import db
from flask_app.db_models import Permission as Permission_db_model

permissions = Blueprint("permissions", __name__)


class PermissionsAPI(MethodView):
    @jwt_required(verify_type=False)
    @superuser_only
    @doc.validate(
        tags=["permissions"],
        resp=Response(
            HTTP_200=(List[Permission], "Get all permissions"),
            HTTP_403=(Status, "Superuser only"),
        ),
    )
    def get(self):
        roles = get_permissions()
        return [
            Permission(**role.to_dict()).dict() for role in roles
        ], HTTPStatus.OK

    @jwt_required(verify_type=False)
    @superuser_only
    @doc.validate(
        tags=["permissions"],
        json=PermissionCreate,
        resp=Response(
            HTTP_200=(list[Permission], "Create new permission"),
            HTTP_403=(Status, "Superuser only"),
        ),
    )
    def post(self):
        logging.debug(f"PermissionsAPI {self.post.__name__} start")
        creator = PermissionCreator(
            request, Permission, Permission_db_model, db
        )
        result, info = creator.save()
        if result is False:
            logging.info(f"{self.post.__name__} error: {info}")
            return {"status": {info}}, HTTPStatus.BAD_REQUEST
        logging.debug(f"PermissionsAPI {self.post.__name__} end")
        return info, HTTPStatus.CREATED


class PermissionsDetailAPI(MethodView):
    @jwt_required(verify_type=False)
    @superuser_only
    @doc.validate(
        tags=["permissions"],
        resp=Response(
            HTTP_200=(Status, "Permission delete"),
            HTTP_404=("", "Permission does not exist"),
            HTTP_403=(Status, "Superuser only"),
        ),
    )
    def delete(self, permission_id):
        logging.debug(f"PermissionsDetailAPI {self.delete.__name__} start")
        permission = db.session.get(Permission_db_model, permission_id)
        if permission is None:
            logging.info(f"{self.delete.__name__} error: NOT_FOUND")
            return "", HTTPStatus.NOT_FOUND
        result, info = dell_obj(db, [permission])
        if result is False:
            return {"status": info}, HTTPStatus.BAD_REQUEST
        logging.debug(f"PermissionsDetailAPI {self.delete.__name__} end")
        return {"status": "success"}, HTTPStatus.OK

    @jwt_required(verify_type=False)
    @superuser_only
    @doc.validate(
        tags=["permissions"],
        resp=Response(
            HTTP_200=(Permission, "Permission update"),
            HTTP_403=(Status, "Superuser only"),
            HTTP_404=("", "Permission does not exist"),
        ),
    )
    def patch(self, permission_id):
        logging.debug(f"PermissionsDetailAPI {self.patch.__name__} start")
        permission = db.session.get(Permission_db_model, permission_id)
        if permission is None:
            return "", HTTPStatus.NOT_FOUND
        new_data = request.get_json()
        updater = PermissionUpdater(
            new_data, Permission, Permission_db_model, db, permission
        )
        result, info = updater.update()
        if result is False:
            logging.info(f"{self.patch.__name__} error: {info}")
            return {"status": info}, HTTPStatus.BAD_REQUEST
        logging.debug(f"PermissionsDetailAPI {self.patch.__name__} end")
        return info, HTTPStatus.OK


permissions.add_url_rule("/", view_func=PermissionsAPI.as_view("permissions"))
permissions.add_url_rule(
    "/<path:permission_id>/",
    view_func=PermissionsDetailAPI.as_view("permission_detail"),
)
