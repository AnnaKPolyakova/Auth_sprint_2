import logging
from http import HTTPStatus

from flask import Blueprint, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from spectree import Response

from flask_app.api.v1.models.common import Status
from flask_app.api.v1.models.role import Role, UserRole, UserRoleCreate
from flask_app.api.v1.utils.other import doc, superuser_only
from flask_app.api.v1.utils.managers import dell_obj
from flask_app.api.v1.utils.user_role import get_user_roles, UserRoleCreator
from flask_app.db import db
from flask_app.db_models import Role as Role_db_model
from flask_app.db_models import User as User_db_model
from flask_app.db_models import UserRoleRelation as UserRoleRelation_db_model

user_roles = Blueprint("user_roles", __name__)


class UserRolesAPI(MethodView):
    @jwt_required(verify_type=False)
    @doc.validate(
        tags=["user_roles"],
        resp=Response(
            HTTP_200=(list[Role], "Get all roles for user"),
            HTTP_404=("", "Object does not exist"),
        ),
    )
    def get(self, user_id):
        logging.debug(f"UserRolesAPI {self.get.__name__} start")
        user = db.session.get(User_db_model, user_id)
        if user is None:
            logging.info(
                f"UserRolesAPI {self.get.__name__} NOT_FOUND"
            )
            return '', HTTPStatus.NOT_FOUND
        roles = get_user_roles(user)
        logging.debug(f"UserRolesAPI {self.get.__name__} end")
        return [Role(**role.to_dict()).dict() for role in roles], HTTPStatus.OK

    @jwt_required(verify_type=False)
    @superuser_only
    @doc.validate(
        tags=["user_roles"],
        json=UserRoleCreate,
        resp=Response(
            HTTP_201=(UserRole, "Add role to user"),
            HTTP_403=(Status, "Superuser only"),
            HTTP_404=("", "Object does not exist"),
        ),
    )
    def post(self, user_id):
        logging.debug(f"UserRolesAPI {self.post.__name__} start")
        user = db.session.get(User_db_model, user_id)
        role_id = request.get_json()["role_id"]
        role = db.session.get(Role_db_model, role_id)
        if role is None or user is None:
            return '', HTTPStatus.NOT_FOUND
        if (
            UserRoleRelation_db_model.query.filter_by(
                user_id=user_id, role_id=role_id
            ).count()
            > 0
        ):
            logging.info(
                f"UserRolesAPI {self.post.__name__} BAD_REQUEST"
            )
            return {
                       "status": "User already have this role"
                   }, HTTPStatus.BAD_REQUEST
        creator = UserRoleCreator(
            {"user_id": user_id, "role_id": role_id},
            UserRole, UserRoleRelation_db_model, db
        )
        result, info = creator.save()
        if result is False:
            logging.info(
                f"UserRolesAPI {self.post.__name__} BAD_REQUEST"
            )
            return {"status": info}, HTTPStatus.BAD_REQUEST
        logging.debug(f"UserRolesAPI {self.post.__name__} end")
        return info, HTTPStatus.CREATED


class UserRolesDetailAPI(MethodView):
    @jwt_required(verify_type=False)
    @superuser_only
    @doc.validate(
        tags=["user_roles"],
        resp=Response(
            HTTP_200=(Status, "Role were delete for user"),
            HTTP_404=("", "Role does not exist for user"),
            HTTP_403=(Status, "Superuser only"),
        ),
    )
    def delete(self, user_id, role_id):
        logging.debug(f"UserRolesDetailAPI {self.delete.__name__} start")
        user = db.session.get(User_db_model, user_id)
        role = db.session.get(Role_db_model, role_id)
        if role is None or user is None:
            return '', HTTPStatus.NOT_FOUND
        user_role = UserRoleRelation_db_model.query.filter_by(
            role_id=role_id, user_id=user_id
        ).first()
        if user_role is None:
            logging.info(
                f"UserRolesDetailAPI {self.delete.__name__} BAD_REQUEST"
            )
            return {
                       "status": "User does not have this role"
                   }, HTTPStatus.BAD_REQUEST
        result, info = dell_obj(db, [user_role])
        if result is False:
            logging.info(
                f"UserRolesDetailAPI {self.delete.__name__} BAD_REQUEST"
            )
            return {"status": info}, HTTPStatus.BAD_REQUEST
        logging.debug(f"UserRolesDetailAPI {self.delete.__name__} end")
        return {"status": "success"}, HTTPStatus.OK


user_roles.add_url_rule("/", view_func=UserRolesAPI.as_view("user_roles"))
user_roles.add_url_rule(
    "/<path:role_id>/",
    view_func=UserRolesDetailAPI.as_view("user_roles_detail")
)
