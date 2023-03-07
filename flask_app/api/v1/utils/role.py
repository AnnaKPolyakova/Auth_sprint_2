from flask_app.api.v1.utils.managers import ObjCreator, ObjUpdater
from flask_app.db_models import Role as Roles_db_model


class RoleCreator(ObjCreator):
    pass


class RoleUpdater(ObjUpdater):
    pass


def get_roles():
    return Roles_db_model.query.all()
