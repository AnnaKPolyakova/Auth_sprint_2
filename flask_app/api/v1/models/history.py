from flask_app.api.v1.models.common import CreateAtMixin, IDAndConfigMixin


class LoginHistory(IDAndConfigMixin, CreateAtMixin):
    user_id: str
