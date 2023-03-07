from datetime import timedelta

from flask import Flask
from flask_jwt_extended import JWTManager
from pydantic import BaseSettings

from flask_app.api.v1.permission import permissions
from flask_app.api.v1.role_permission import role_permissions
from flask_app.api.v1.roles import roles
from flask_app.api.v1.tokens import tokens
from flask_app.api.v1.user_roles import user_roles
from flask_app.api.v1.users import users
from flask_app.api.v1.utils.other import doc
from flask_app.db import db
from flask_app.db_init import init_db
from flask_app.db_models import User
from flask_app.settings import settings


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
    current_app = Flask(__name__)

    current_app.config["JWT_SECRET_KEY"] = settings.JWT_SECRET_KEY
    current_app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    current_app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    init_db(current_app, settings)
    current_app.register_blueprint(users, url_prefix="/api/v1/users")
    current_app.register_blueprint(tokens, url_prefix="/api/v1/tokens")
    current_app.register_blueprint(roles, url_prefix="/api/v1/roles")
    current_app.register_blueprint(
        user_roles, url_prefix="/api/v1/users/<path:user_id>/roles"
    )
    current_app.register_blueprint(
        permissions, url_prefix="/api/v1/permissions"
    )
    current_app.register_blueprint(
        role_permissions, url_prefix="/api/v1/roles/<path:role_id>/permissions"
    )
    doc.register(current_app)
    create_superuser(current_app)
    return current_app


if __name__ == "__main__":
    app = create_app()
    jwt = JWTManager(app)
    app.run()
