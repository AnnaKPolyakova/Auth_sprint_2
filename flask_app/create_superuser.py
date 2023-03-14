# import logging
#
# import click
# from flask import Blueprint
# from flask.cli import with_appcontext
#
# from flask_app.db_models import User
# from flask_app.db import db
#
#
# user_cli = Blueprint('user', __name__)
#
#
# @user_cli.cli.command('create')
# @click.argument('name')
# @with_appcontext
# def create_is_superuser(name):
#     admin = User(login=name, is_superuser=True)
#     admin.set_password(name)
#     logging.info("is_superuser user was created")
#     try:
#         db.session.add(admin)
#         db.session.commit()
#     except Exception as error:
#         logging.info(error)
#         db.session.rollback()
