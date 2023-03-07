import random
import socket

import requests

from flask_app.api.v1.models.user import User
from flask_app.api.v1.utils.token import get_tokens_for_user
from flask_app.api.v1.utils.user import UserCreator
from flask_app.db import db, redis_db
from flask_app.db_models import User as User_db_model
from flask_app.settings import settings


class AuthManager:
    TOKEN_URI = None
    REDIRECT_URI = None
    USER_INFO_URI = None
    AUTH_URL = None
    CLIENT_ID = None
    SECRET = None
    AUTH_PARAMS = dict()
    USER_INFO_PARAMS = dict()
    TOKEN_DATA = dict()

    def __init__(self):
        self.full_auth_param = dict()
        self.full_token_data = dict()
        self.full_info_param = dict()

    def _set_full_auth_param(self):
        self.full_auth_param = self.AUTH_PARAMS
        self.full_auth_param[
            "redirect_uri"
        ] = "http://127.0.0.1:5000" + self.REDIRECT_URI
        # ] = socket.gethostname() + self.REDIRECT_URI

    def _set_full_user_info_param(self, token):
        self.full_info_param = self.USER_INFO_PARAMS
        jwt_secret = token
        self.full_info_param["oauth_token"] = jwt_secret

    def _set_full_token_data(self, code):
        self.full_token_data = self.TOKEN_DATA
        self.full_token_data["code"] = code

    def get_redirect_uri(self):
        self._set_full_auth_param()
        return requests.get(self.AUTH_URL, params=self.full_auth_param).url

    @staticmethod
    def _create_user(data, email):
        user_data = {
            "login": data["login"] + "_" + str(random.random()),
            "email": email,
            "is_superuser": False,
            "password": str(random.random())
        }
        creator = UserCreator(user_data, User, User_db_model, db)
        result, _ = creator.save()
        if result is False:
            return None
        return creator.obj

    def _get_token_data(self, code):
        self._set_full_token_data(code)
        response = requests.post(
            self.TOKEN_URI, data=self.full_token_data
        )
        return response.json()

    def _get_or_create_user(self, token):
        pass

    @staticmethod
    def _save_access_token_to_redis(user, token, expired):
        redis_db.set(
            name=str(user.id),
            value=token,
            ex=expired
        )

    @staticmethod
    def _get_token_from_data(data):
        pass

    @staticmethod
    def _get_expired_from_data(data):
        pass

    def get_tokens_for_user(self, code):
        data = self._get_token_data(code)
        token = self._get_token_from_data(data)
        if token is None:
            return dict()
        user = self._get_or_create_user(token)
        if user is None:
            return dict()
        expired = self._get_expired_from_data(data)
        self._save_access_token_to_redis(user, token, expired)
        return get_tokens_for_user(user)


class YandexAuthManager(AuthManager):
    TOKEN_URI = settings.TOKEN_URL_YANDEX
    REDIRECT_URI = "/api/v1/social/complete/yandex/"
    USER_INFO_URI = settings.USER_INFO_URL_YANDEX
    AUTH_URL = settings.AUTH_URL_YANDEX
    CLIENT_ID = settings.CLIENT_ID_YANDEX
    SECRET = settings.SECRET_YANDEX
    AUTH_PARAMS = {
        "response_type": "code",
        "client_id": CLIENT_ID,
    }
    TOKEN_DATA = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": SECRET,
    }
    USER_INFO_PARAMS = {
        "format": "json"
    }

    def _get_or_create_user(self, token):
        self._set_full_user_info_param(token)
        response = requests.get(
            self.USER_INFO_URI, params=self.full_info_param
        )
        data = response.json()
        emails = data.get("emails", None)
        user = User_db_model.query.filter(
            User_db_model.email.in_(emails)
        ).first()
        if user is None:
            user = self._create_user(data, emails[0])
        return user

    @staticmethod
    def _get_token_from_data(data):
        return data.get("access_token", None)

    @staticmethod
    def _get_expired_from_data(data):
        return data.get("expires_in", None)


PROVIDERS_AND_MANAGERS = {
    "yandex": YandexAuthManager
}