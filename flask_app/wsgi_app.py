from flask import request
from flask_jwt_extended import JWTManager
from gevent import monkey
from opentelemetry.instrumentation.flask import FlaskInstrumentor

from flask_app.tracer import configure_tracer

monkey.patch_all()

from flask_app.app import create_app

app = create_app()
jwt = JWTManager(app)


configure_tracer()
FlaskInstrumentor().instrument_app(app)


@app.before_request
def before_request():
    request_id = request.headers.get("X-Request-Id")
    if not request_id:
        raise RuntimeError("request id is required")
