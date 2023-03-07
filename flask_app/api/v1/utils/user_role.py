from flask_app.api.v1.utils.managers import ObjCreator


class UserRoleCreator(ObjCreator):
    pass


def get_user_roles(user):
    return user.roles
