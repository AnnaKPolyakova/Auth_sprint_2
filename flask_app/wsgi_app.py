from flask_jwt_extended import JWTManager
from gevent import monkey

monkey.patch_all()

from flask_app.app import create_app

app = create_app()
jwt = JWTManager(app)
