from flask import Flask
from pydantic import BaseSettings

from flask_app.db import db


def init_db(app: Flask, settings: BaseSettings):
    uri_template = "postgresql://{username}:{password}@{host}/{database_name}"
    uri = uri_template.format(
        username=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        database_name=settings.POSTGRES_DB,
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    db.init_app(app)
    app.app_context().push()
    db.create_all()
    return db
