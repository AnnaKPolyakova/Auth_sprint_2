import logging
from http import HTTPStatus

import flask
from flask import Blueprint, request
from spectree import Response

from flask_app.api.v1.models.common import Status
from flask_app.api.v1.models.social_auth import SocialAuthCode
from flask_app.api.v1.models.user import Tokens
from flask_app.api.v1.utils.other import doc
from flask_app.api.v1.utils.social_auth import YandexAuthManager, \
    PROVIDERS_AND_MANAGERS

social_login = Blueprint("social_login", __name__)
social_complete = Blueprint("social_complete", __name__)


@social_login.route("/<path:provider>/", methods=["GET"])
@doc.validate(
    tags=["social_auth"],
    resp=Response(
        HTTP_302=(None, "Code were created"),
        HTTP_400=(Status, "Error"),
    ),
)
def yandex_get_auth(provider):
    manager_class = PROVIDERS_AND_MANAGERS.get(provider, None)
    if manager_class is None:
        return {"status": False}, HTTPStatus.BAD_REQUEST
    manager = manager_class()
    return flask.redirect(manager.get_redirect_uri(), code=302, Response=None)


@social_complete.route("/<path:provider>/", methods=["GET"])
@doc.validate(
    tags=["social_auth"],
    query=SocialAuthCode,
    resp=Response(
        HTTP_201=(Tokens, "Status for token"),
        HTTP_400=(Status, "Token creation error"),
        HTTP_403=(Status, "FORBIDDEN"),
    ),
)
def yandex_get_token(provider):
    manager_class = PROVIDERS_AND_MANAGERS.get(provider, None)
    if manager_class is None:
        return {"status": False}, HTTPStatus.BAD_REQUEST
    code = request.args.get("code", default=-1)
    if code == -1:
        return {"status": False}, HTTPStatus.FORBIDDEN
    data = manager_class().get_tokens_for_user(code)
    if len(data) > 0:
        return data, HTTPStatus.CREATED
    return {"status": False}, HTTPStatus.BAD_REQUEST
