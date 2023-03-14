from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


def init_limiter(app: Flask, settings):

    limit = "{limit} per second".format(limit=settings.DEFAULT_LIMITS)
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=[limit],
        storage_uri="redis://{host}:{port}".format(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT
        )
    )
    limiter.init_app(app)
