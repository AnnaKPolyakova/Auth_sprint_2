from datetime import timedelta
from logging.config import dictConfig

from flask import Flask
from flask_jwt_extended import JWTManager
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from pydantic import BaseSettings

from flask_app.api.v1.permission import permissions
from flask_app.api.v1.role_permission import role_permissions
from flask_app.api.v1.roles import roles
from flask_app.api.v1.social_auth import social_login, social_complete
from flask_app.api.v1.tokens import tokens
from flask_app.api.v1.user_roles import user_roles
from flask_app.api.v1.users import users
from flask_app.api.v1.utils.other import doc
from flask_app.commands import create_is_superuser
from flask_app.db import db
from flask_app.db_init import init_db
from flask_app.db_models import User
from flask_app.init_limiter import init_limiter
from flask_app.settings import settings
from flask_app.tracer import configure_tracer


def create_superuser(app):
    admin = User(login="admin", is_superuser=True)
    admin.set_password("admin")
    app.logger.info("admin user was created")
    try:
        db.session.add(admin)
        db.session.commit()
    except Exception as error:
        app.logger.info(error)
        db.session.rollback()


def create_app(settings: BaseSettings = settings):
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
    current_app = Flask("auth_app")

    current_app.config["JWT_SECRET_KEY"] = settings.JWT_SECRET_KEY
    current_app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    current_app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    init_db(current_app, settings)
    current_app.register_blueprint(users, url_prefix="/api/v1/users")
    current_app.register_blueprint(tokens, url_prefix="/api/v1/tokens")
    current_app.register_blueprint(roles, url_prefix="/api/v1/roles")
    current_app.register_blueprint(
        social_login, url_prefix="/api/v1/social/login"
    )
    current_app.register_blueprint(
        social_complete, url_prefix="/api/v1/social/complete"
    )
    current_app.register_blueprint(
        user_roles, url_prefix="/api/v1/users/<path:user_id>/roles"
    )
    current_app.register_blueprint(
        permissions, url_prefix="/api/v1/permissions"
    )
    current_app.register_blueprint(
        role_permissions, url_prefix="/api/v1/roles/<path:role_id>/permissions"
    )
    current_app.cli.add_command(create_is_superuser)
    doc.register(current_app)
    create_superuser(current_app)
    init_limiter(current_app, settings)
    return current_app


if __name__ == "__main__":
    if settings.TRACER_ON:
        configure_tracer()
    app = create_app()
    FlaskInstrumentor().instrument_app(app)
    jwt = JWTManager(app)
    app.run(host='0.0.0.0')
