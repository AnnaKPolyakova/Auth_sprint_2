import logging
from http import HTTPStatus

from flask import Blueprint, current_app, request
from flask_jwt_extended import (
    get_jwt, get_jwt_identity, jwt_required
)
from spectree import Response

from flask_app.api.v1.models.common import Status
from flask_app.api.v1.models.user import (
    AccessTokens, Tokens, UserLogin, UserId
)
from flask_app.api.v1.utils.history import HistoryCreator
from flask_app.api.v1.utils.other import doc
from flask_app.api.v1.utils.token import get_access_tokens, get_tokens_for_user
from flask_app.db import db, jwt_redis_blocklist
from flask_app.db_models import LoginHistory
from flask_app.db_models import User as Users_db_model

tokens = Blueprint("tokens", __name__)


@tokens.route("/", methods=["POST"])
@doc.validate(
    tags=["token"],
    json=UserLogin,
    resp=Response(
        HTTP_201=(Tokens, "Tokens were created"),
        HTTP_400=(Status, "Error"),
    ),
)
def get_tokens():
    logging.debug(f"TokenAPI {get_tokens.__name__} start")
    user = Users_db_model.query.filter_by(
        login=request.get_json()["login"]
    ).first()
    if user is None:
        logging.info(f"TokenAPI {get_tokens.__name__} BAD_REQUEST")
        return {"status": "User does not exist"}, HTTPStatus.BAD_REQUEST
    if user.check_password(request.get_json()["password"]) is False:
        logging.info(f"TokenAPI {get_tokens.__name__} BAD_REQUEST")
        return {"status": "Error password"}, HTTPStatus.BAD_REQUEST
    creator = HistoryCreator({"user_id": user.id}, UserId, LoginHistory, db)
    result, info = creator.save()
    if result is False:
        logging.info(f"TokenAPI {get_tokens.__name__} BAD_REQUEST")
        return {"status": {info}}, HTTPStatus.BAD_REQUEST
    tokens_data = get_tokens_for_user(user)
    logging.debug(f"TokenAPI {get_tokens.__name__} end")
    return Tokens(**tokens_data).dict(), HTTPStatus.CREATED


@tokens.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
@doc.validate(
    tags=["token"],
    resp=Response(
        HTTP_201=(AccessTokens, "Tokens were created"),
        HTTP_400=(Status, "Error"),
    ),
    security=[{"auth_oauth2": ["read"]}],
)
def refresh():
    logging.debug(f"TokenAPI {refresh.__name__} start")
    identity = get_jwt_identity()
    data = get_access_tokens(identity)
    logging.debug(f"TokenAPI {refresh.__name__} end")
    return data, HTTPStatus.CREATED


@tokens.route("/logout", methods=["DELETE"])
@doc.validate(
    tags=["token"],
    resp=Response(
        HTTP_200=(Status, "Logout were done"),
    ),
    security=[{"auth_oauth2": ["read"]}],
)
@jwt_required(verify_type=False)
def logout():
    logging.debug(f"TokenAPI {logout.__name__} start")
    token = get_jwt()
    jti = token["jti"]
    jwt_redis_blocklist.set(
        jti, "", ex=current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
    )
    logging.debug(f"TokenAPI {logout.__name__} end")
    return {"status": "success"}, HTTPStatus.OK
