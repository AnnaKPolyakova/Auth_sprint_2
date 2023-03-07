from flask_app.api.v1.utils.managers import ObjCreator, ObjUpdater

from flask_app.db_models import User as Users_db_model


class UserCreator(ObjCreator):

    def save(self, is_superuser=False):
        self.obj.is_superuser = is_superuser
        self.obj.set_password()
        return self._save_obj()


def get_users():
    return Users_db_model.query.all()


class UserUpdater(ObjUpdater):

    def _update_obj(self):
        for field, value in self.new_data.items():
            if field == "password":
                self.obj.set_password(value)
                continue
            setattr(self.obj, field, value)
