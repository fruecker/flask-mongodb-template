
import flask
from flask import Blueprint

from flask_login import login_required

from app.decorators import admin_only
from app.utils.sites import site_map


# Import module forms
module_default = Blueprint("default", __name__)

@module_default.route("/")
def home():
    return flask.render_template("home.html")

@module_default.route("/routes")
def routes():
    links = site_map()
    links.extend(
        [
            # ("/api/v1/...", "blabla")
        ]
    )
    return flask.render_template("routes.html", links=links)
