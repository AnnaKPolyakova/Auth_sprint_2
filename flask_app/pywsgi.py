from flask_jwt_extended import JWTManager
from gevent import monkey

monkey.patch_all()

from gevent.pywsgi import WSGIServer
from flask_app.app import create_app

app = create_app()
jwt = JWTManager(app)

if __name__ == "__main__":
    http_server = WSGIServer(("", 5000), app)
    http_server.serve_forever()
