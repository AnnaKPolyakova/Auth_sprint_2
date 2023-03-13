import logging

from flask import Blueprint, request
from auth_proxy_app.proxy_manager import ProxyManager
from auth_proxy_app.utils import auth_proxy_doc

auth_proxy = Blueprint("auth_proxy", __name__)


@auth_proxy.route(
    '/<path:path>/', methods=["POST", "GET", "PATCH", "PUT", "DELETE"]
)
@auth_proxy_doc.validate(
    tags=["auth_proxy"],
)
def auth(path):
    logging.debug("auth_proxy {name} start".format(name=auth.__name__))
    result, status = ProxyManager(request).get_request()
    return result, status
