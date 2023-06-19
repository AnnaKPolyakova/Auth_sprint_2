import logging

import click

from flask_app.db import db
from flask_app.db_models import User


@click.command('is_superuser_create')
@click.argument('name')
def create_is_superuser(name):
    admin = User(login=name, is_superuser=True)
    admin.set_password(name)
    logging.info("is_superuser user was created")
    try:
        db.session.add(admin)
        db.session.commit()
    except Exception as error:
        logging.info(error)
        db.session.rollback()
