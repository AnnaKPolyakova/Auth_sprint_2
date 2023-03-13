from flask_jwt_extended import JWTManager
from gevent import monkey

monkey.patch_all()

from auth_proxy_app.app_proxy import create_auth_proxy_app

app = create_auth_proxy_app()
jwt = JWTManager(app)
