import uuid
from http import HTTPStatus

import requests
from flask import request as flask_request

from auth_proxy_app.db import redis_db
from auth_proxy_app.settings import auth_proxy_settings

URL_KEYS = [
    "create_is_superuser",
    "check_permission",
    "login_history",
    "logout",
    "refresh",
    "tokens",
    "users",
    "roles",
    "social",
    "permissions"
]


class ProxyManager:

    def __init__(self, request: flask_request):
        from auth_proxy_app.wsgi_app import app
        self.logging = app.logger
        self.request = request
        self.token = request.headers.environ.get('HTTP_AUTHORIZATION', None)
        self.data = self._get_data(request)
        self.url = self._get_url(request)
        self.method = request.method.lower()
        self.params = dict(self.request.args)
        self.x_request_id = request.headers.environ.get(
            'X-Request-Id', str(uuid.uuid4())
        )

    @staticmethod
    def _get_data(request):
        try:
            return request.json
        except Exception:
            return dict()

    @staticmethod
    def _get_url(request):
        return auth_proxy_settings.AUTH_HOST + \
               "/" + request.view_args["path"] + "/"

    def _get_method(self):
        method = self.data['method']
        del self.data['method']
        return method

    def _get_db_key(self):
        url_list = self.url.split('/')
        for key in URL_KEYS:
            if key in url_list:
                return key
        return ""

    def _sent_request_to_auth(self):
        self.logging.debug(
            "Start sent_request_to_auth, url: {url}".format(url=self.url)
        )
        response = getattr(requests, self.method)(
            self.url,
            headers={
                "Authorization": self.token,
                "X-Request-Id": self.x_request_id
            },
            json=self.data,
            params=self.params,
            timeout=auth_proxy_settings.TIMOUT_FOR_REQUEST
        )
        self.logging.debug(
            "response: {response}".format(response=response)
        )
        return response

    @staticmethod
    def _save_new_errors_count(key, counter):
        if key is None:
            return {"status": False}, HTTPStatus.BAD_REQUEST
        redis_db.set(
            name=key, value=counter + 1, ex=int(auth_proxy_settings.EX_TIME)
        )

    def get_request(self):
        self.logging.debug("Start logging")
        if self.url is None or self.method is None:
            self.logging.info(
                "url: {url} or method: {method} is None".format(
                    url=self.url,
                    method=self.method,
                )
            )
            return {"status: False"}, HTTPStatus.BAD_REQUEST
        key = self._get_db_key()
        self.logging.debug("key: {key}".format(key=key))
        counter = redis_db.get(name=key)
        self.logging.debug("counter: {counter}".format(counter=counter))
        if counter is None:
            counter = 0
        else:
            counter = int(counter)
        self.logging.debug(
            "MAX_REQUEST_COUNT: "
            "{MAX_REQUEST_COUNT}".format(
                MAX_REQUEST_COUNT=auth_proxy_settings.MAX_REQUEST_COUNT)
        )
        if counter > auth_proxy_settings.MAX_REQUEST_COUNT:
            self.logging.info(
                "Error counter {counter} more then {max_count}".format(
                    counter=counter,
                    max_count=auth_proxy_settings.MAX_REQUEST_COUNT
                )
            )
            return {"status": False}, HTTPStatus.BAD_REQUEST
        try:
            response = self._sent_request_to_auth()
        except Exception as error:
            self.logging.error(
                "Request to auth get error: {error}".format(error=error)
            )
            self._save_new_errors_count(key, counter)
            return {"status": False}, HTTPStatus.BAD_REQUEST
        if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
            self.logging.error("Internal_server_error")
            return {"status": False}, HTTPStatus.BAD_REQUEST
        return response.text, response.status_code
