from flask_jwt_extended import JWTManager
from gevent import monkey

monkey.patch_all()

from auth_proxy_app.app_proxy import create_auth_proxy_app

from gevent.pywsgi import WSGIServer

app = create_auth_proxy_app()
jwt = JWTManager(app)

if __name__ == "__main__":
    http_server = WSGIServer(("", 8001), app)
    http_server.serve_forever()
