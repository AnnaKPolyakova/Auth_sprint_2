from flask_app.db_models import Permission as Permission_db_model
from flask_app.api.v1.utils.managers import ObjCreator, ObjUpdater


class PermissionCreator(ObjCreator):
    pass


class PermissionUpdater(ObjUpdater):
    pass


def check_permission_for_user(user, permission_id):
    roles = user.roles
    for role in roles:
        if permission_id in [str(p.id) for p in role.permissions]:
            return True
    return False


def get_permissions():
    return Permission_db_model.query.all()
