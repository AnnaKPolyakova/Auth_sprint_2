import logging
from http import HTTPStatus

from flask import Blueprint, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from spectree import Response

from flask_app.api.v1.models.common import Status
from flask_app.api.v1.models.role import Role, RoleCreate
from flask_app.api.v1.utils.managers import dell_obj
from flask_app.api.v1.utils.other import doc, superuser_only
from flask_app.api.v1.utils.role import RoleCreator, RoleUpdater, get_roles
from flask_app.db import db
from flask_app.db_models import Role as Roles_db_model

roles = Blueprint("roles", __name__)


class RoleAPI(MethodView):
    @jwt_required(verify_type=False)
    @superuser_only
    @doc.validate(
        tags=["roles"],
        resp=Response(
            HTTP_200=(list[Role], "Get all roles"),
            HTTP_403=(Status, "Superuser only")
        ),
    )
    def get(self):
        logging.debug(f"RoleAPI {self.get.__name__} start")
        roles = get_roles()
        logging.debug(f"RoleAPI {self.get.__name__} end")
        return [Role(**role.to_dict()).dict() for role in roles], HTTPStatus.OK

    @jwt_required(verify_type=False)
    @superuser_only
    @doc.validate(
        tags=["roles"],
        json=RoleCreate,
        resp=Response(
            HTTP_201=(Role, "Create new role"),
            HTTP_403=(Status, "Superuser only"),
        ),
    )
    def post(self):
        logging.debug(f"RoleAPI {self.post.__name__} start")
        creator = RoleCreator(request, Role, Roles_db_model, db)
        result, info = creator.save()
        if result is False:
            logging.info(f"RoleAPI {self.post.__name__} BAD_REQUEST")
            return {"status": {info}}, HTTPStatus.BAD_REQUEST
        logging.debug(f"RoleAPI {self.post.__name__} end")
        return info, HTTPStatus.CREATED


class RoleDetailAPI(MethodView):
    @jwt_required(verify_type=False)
    @superuser_only
    @doc.validate(
        tags=["roles"],
        resp=Response(
            HTTP_200=(Status, "Role delete"),
            HTTP_404=("", "Role does not exist"),
            HTTP_403=(Status, "Superuser only"),
        ),
    )
    def delete(self, role_id):
        logging.debug(f"RoleDetailAPI {self.delete.__name__} start")
        role = db.session.get(Roles_db_model, role_id)
        if role is None:
            logging.info(f"RoleDetailAPI {self.delete.__name__} BAD_REQUEST")
            return {"status": "is not owner"}, HTTPStatus.BAD_REQUEST
        objs = [role]
        result, info = dell_obj(db, objs)
        if result is False:
            logging.info(f"RoleDetailAPI {self.delete.__name__} BAD_REQUEST")
            return {"status": info}, HTTPStatus.BAD_REQUEST
        logging.debug(f"RoleDetailAPI {self.delete.__name__} end")
        return {"status": "success"}, HTTPStatus.OK

    @jwt_required(verify_type=False)
    @superuser_only
    @doc.validate(
        tags=["roles"],
        resp=Response(
            HTTP_200=(Role, "Role update"), HTTP_403=(Status, "Superuser only")
        ),
    )
    def patch(self, role_id):
        logging.debug(f"RoleDetailAPI {self.patch.__name__} start")
        role = db.session.get(Roles_db_model, role_id)
        if role is None:
            logging.info(f"RoleDetailAPI {self.patch.__name__} BAD_REQUEST")
            return {"status": "is not owner"}, HTTPStatus.BAD_REQUEST
        new_data = request.get_json()
        updater = RoleUpdater(new_data, Role, Roles_db_model, db, role)
        result, info = updater.update()
        if result is False:
            return {"status": info}, HTTPStatus.BAD_REQUEST
        logging.debug(f"RoleDetailAPI {self.patch.__name__} end")
        return info, HTTPStatus.OK


roles.add_url_rule("/", view_func=RoleAPI.as_view("roles"))
roles.add_url_rule(
    "/<path:role_id>/",
    view_func=RoleDetailAPI.as_view("roles_detail")
)
