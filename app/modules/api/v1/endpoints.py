
import flask
from flask import Blueprint, request

from flask_login import login_required
from app.database.models.user import User

from app.decorators import admin_only, under_construction
from app.utils.ip import get_public_ip
from app.utils.sites import site_map


# Import module forms
module_api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")

@module_api_v1.route("/")
def running():
    return "API v1 is up and running!"


@module_api_v1.route('/ip')
def get_ip():
    """Returns the current ip address of the server"""
    ip_address_remote = request.remote_addr
    ip_address_public = get_public_ip()
    return flask.jsonify(remote_ip=ip_address_remote, public_ip=ip_address_public)


@module_api_v1.route("/routes")
@under_construction
def routes():
    return flask.jsonify(site_map())


@module_api_v1.route("/test", methods=["GET","POST", "PUT", "DELETE"])
def test():
    method = request.method
    headers = request.headers
    data = request.data
    json = request.get_json(silent=True)
    print("Methode:", method)
    print("Headers:", headers)
    print("Json:", json)
    print("Data:", data)
    return flask.jsonify(methode=method, json=json)