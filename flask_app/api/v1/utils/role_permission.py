from flask_app.api.v1.utils.managers import ObjCreator


class RolePermissionCreator(ObjCreator):
    pass


def get_role_permissions(role):
    return role.permissions
