import logging
import time
import uuid
from http import HTTPStatus

from flask import Blueprint, request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from spectree import Response

from flask_app.api.v1.models.common import ResultBool, Status, UserId
from flask_app.api.v1.models.history import LoginHistory
from flask_app.api.v1.models.permission import CheckPermission, Page, \
    FieldAndPage
from flask_app.api.v1.models.user import User, UserCreate, UserIds, UserUpdate
from flask_app.api.v1.utils.history import get_histories
from flask_app.api.v1.utils.other import doc, superuser_only
from flask_app.api.v1.utils.permission import check_permission_for_user
from flask_app.api.v1.utils.user import (
    UserCreator,
    UserUpdater,
    get_data_for_users_list,
    get_users, get_users_values_dict,
)
from flask_app.db import db
from flask_app.db_models import User as Users_db_model

users = Blueprint("users", __name__)


class UserAPI(MethodView):
    @doc.validate(
        tags=["user"],
        resp=Response("HTTP_200", HTTP_200=(list[User], "Get all users")),
    )
    def get(self):
        logging.debug(f"UserAPI {self.get.__name__} start")
        users_all = get_users()
        if users_all is None:
            logging.info(
                f"UserAPI {self.get.__name__} User not found. Check uuid"
            )
            return {"message": "User not found. Check uuid"}
        logging.debug(f"UserAPI {self.get.__name__} end")
        return [
            User(**user.to_dict()).dict() for user in users_all
        ], HTTPStatus.OK

    @doc.validate(
        tags=["user"],
        json=UserCreate,
        resp=Response(
            HTTP_201=(User, "Create user"), HTTP_400=(Status, "Error")
        ),
    )
    def post(self):
        logging.debug(f"UserAPI {self.post.__name__} start")
        if (
            Users_db_model.query.filter_by(
                login=request.get_json()["login"]
            ).count() > 0
        ):
            logging.info(f"UserAPI {self.post.__name__} already exist")
            return {"status": "already exist"}, HTTPStatus.BAD_REQUEST
        creator = UserCreator(request, User, Users_db_model, db)
        result, info = creator.save()
        if result is False:
            logging.info(f"UserAPI {self.post.__name__} BAD_REQUEST")
            return {"status": info}, HTTPStatus.BAD_REQUEST
        logging.debug(f"UserAPI {self.post.__name__} end")
        return info, HTTPStatus.CREATED


@users.route("/users_data/", methods=["POST"])
@doc.validate(
    tags=["user"],
    json=UserIds,
    query=FieldAndPage,
    resp=Response("HTTP_200"),
)
def get_users_data():
    logging.debug(f"UserAPI {get_users_data.__name__} start")
    page = request.args.get("page", default=1, type=int)
    field = request.args.get("field", default="mail", type=str)
    users_data = get_data_for_users_list(
        request.get_json()["ids"], page
    )
    data = get_users_values_dict(users_data, User, field)
    logging.debug(f"UserAPI {get_users_data.__name__} end")
    return data, HTTPStatus.OK


class UserDetailAPI(MethodView):
    @jwt_required(verify_type=False)
    @doc.validate(
        tags=["user"],
        json=UserUpdate,
        resp=Response(
            HTTP_200=(User, "Update user"), HTTP_400=(Status, "Error")
        ),
    )
    def patch(self, user_id):
        logging.debug(f"UserDetailAPI {self.patch.__name__} start")
        id = get_jwt_identity()
        user = db.session.get(Users_db_model, id)
        if user is None or str(user.id) != user_id:
            logging.info(
                f"UserAPI {self.patch.__name__} is not owner or not exist"
            )
            return {
                "status": "is not owner or not exist"
            }, HTTPStatus.BAD_REQUEST
        new_data = request.get_json()
        updater = UserUpdater(new_data, User, UserUpdate, db, user)
        result, info = updater.update()
        if result is False:
            logging.info(f"UserAPI {self.patch.__name__} BAD_REQUEST")
            return {"status": info}, HTTPStatus.BAD_REQUEST
        logging.debug(f"UserDetailAPI {self.patch.__name__} end")
        return info, HTTPStatus.OK

    @doc.validate(
        tags=["user"],
        resp=Response(HTTP_200=(User, "Get user"), HTTP_400=(Status, "Error")),
    )
    def get(self, user_id):
        logging.debug(f"UserDetailAPI {self.get.__name__} start")
        try:
            uuid.UUID(user_id)
        except Exception:
            return {"status": "user id invalid"}, HTTPStatus.BAD_REQUEST
        user = db.session.get(Users_db_model, user_id)
        if user is None or str(user.id) != user_id:
            logging.info(
                f"UserAPI {self.patch.__name__} is not owner or not exist"
            )
            return {"status": "not exist"}, HTTPStatus.NOT_FOUND
        logging.debug(f"UserDetailAPI {self.get.__name__} end")
        return User(**user.to_dict()).dict(), HTTPStatus.OK


@users.route("/login_history/", methods=["GET"])
@jwt_required(verify_type=False)
@doc.validate(
    tags=["history"],
    query=Page,
    resp=Response(HTTP_200=(list[LoginHistory], "Get all histories for user")),
)
def histories_get():
    logging.debug(f"UserDetailAPI {histories_get.__name__} start")
    page = request.args.get("page", default=1, type=int)
    user_id = get_jwt_identity()
    user = db.session.get(Users_db_model, user_id)
    if user is None:
        logging.info(f"UserAPI {histories_get.__name__} is not owner")
        return {"status": "is not owner"}, HTTPStatus.BAD_REQUEST
    histories = get_histories(user, page)
    logging.debug(f"UserDetailAPI {histories_get.__name__} end")
    return [
        LoginHistory(**history.to_dict()).dict() for history in histories
    ], HTTPStatus.OK


@users.route("/<path:user_id>/check_permission/", methods=["POST"])
@doc.validate(
    tags=["user"],
    json=CheckPermission,
    resp=Response(
        HTTP_200=(ResultBool, "Check permission for user"),
        HTTP_404=(Status, "Bad request"),
    ),
)
def check_permission(user_id):
    logging.debug(f"UserDetailAPI {check_permission.__name__} start")
    user = db.session.get(Users_db_model, user_id)
    if user is None:
        logging.info(f"UserAPI {check_permission.__name__} User not exist")
        return {"status": "User not exist"}, HTTPStatus.BAD_REQUEST
    permission_id = request.get_json()["permission_id"]
    result = check_permission_for_user(user, permission_id)
    logging.debug(f"UserDetailAPI {check_permission.__name__} end")
    return {"result": result}, HTTPStatus.OK


@users.route("/create_is_superuser/", methods=["POST"])
@jwt_required(verify_type=False)
@superuser_only
@doc.validate(
    tags=["user"],
    json=UserCreate,
    resp=Response(
        HTTP_201=(User, "Create is_superuser"), HTTP_400=(Status, "Error")
    ),
)
def create_is_superuser():
    logging.debug(f"UserDetailAPI {create_is_superuser.__name__} start")
    if Users_db_model.query.filter_by(
            login=request.get_json()["login"]
    ).count() > 0:
        logging.info(
            f"UserDetailAPI {create_is_superuser.__name__} already exist"
        )
        return {"status": "already exist"}, HTTPStatus.BAD_REQUEST
    creator = UserCreator(request, User, Users_db_model, db)
    result, info = creator.save(True)
    if result is False:
        logging.info(
            f"UserDetailAPI {create_is_superuser.__name__} BAD_REQUEST"
        )
        return {"status": info}, HTTPStatus.BAD_REQUEST
    logging.debug(f"UserDetailAPI {create_is_superuser.__name__} end")
    return info, HTTPStatus.CREATED


@users.route("/auth_check/", methods=["GET"])
@jwt_required(verify_type=False)
@doc.validate(
    tags=["user"],
    resp=Response(
        HTTP_200=(UserId, "Auth check passed"),
    ),
)
def auth_check():
    logging.debug("start auth_check")
    user_id = get_jwt_identity()
    return {"id": user_id}, HTTPStatus.OK


@users.route("/wait/", methods=["POST"])
@doc.validate(
    tags=["user"],
)
def wait():
    time.sleep(10)
    return {}, HTTPStatus.CREATED


users.add_url_rule("/", view_func=UserAPI.as_view("users"))
users.add_url_rule(
    "/<path:user_id>/", view_func=UserDetailAPI.as_view("users_detail")
)
