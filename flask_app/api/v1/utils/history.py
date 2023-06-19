from flask_app.api.v1.utils.managers import ObjCreator
from flask_app.db_models import LoginHistory as LoginHistory_db_model
from flask_app.settings import settings


class HistoryCreator(ObjCreator):
    pass


def get_histories(user, page):
    return LoginHistory_db_model.query.filter_by(
        user_id=user.id
    ).paginate(page=page, per_page=settings.PAGE_SIZE)
