from datetime import timedelta
from logging.config import dictConfig

from flask import Flask
from flask_jwt_extended import JWTManager
from pydantic import BaseSettings

from auth_proxy_app.api import auth_proxy
from auth_proxy_app.settings import auth_proxy_settings
from auth_proxy_app.utils import auth_proxy_doc


def create_auth_proxy_app(settings: BaseSettings = auth_proxy_settings):
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'DEBUG',
            'handlers': ['wsgi']
        }
    })
    current_app = Flask(__name__)
    current_app.config["JWT_SECRET_KEY"] = settings.JWT_SECRET_KEY
    current_app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    current_app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    current_app.register_blueprint(auth_proxy, url_prefix="")
    auth_proxy_doc.register(current_app)
    return current_app


if __name__ == "__main__":
    app = create_auth_proxy_app()
    jwt = JWTManager(app)
    app.run(port=8001)
