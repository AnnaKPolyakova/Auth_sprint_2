from functools import wraps
from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity
from spectree import SpecTree

from flask_app.db import db
from flask_app.db_models import User

doc = SpecTree(
    "flask", title='Auth API documentation', version='v1', path='v1/doc/'
)


def superuser_only(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        if user is None:
            return '', HTTPStatus.NOT_FOUND
        if user.is_superuser is False:
            return {
                       "status": "Method is only for is_superusers"
                   }, HTTPStatus.FORBIDDEN
        return func(*args, **kwargs)

    return wrapped
