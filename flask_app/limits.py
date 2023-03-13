from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from flask_app.settings import settings

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["1 per second"],
    storage_uri="redis://{host}:{port}".format(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT
    )
)


def init_limiter(app: Flask):
    limiter.init_app(app)
