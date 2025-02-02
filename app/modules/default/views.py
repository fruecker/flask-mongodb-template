
import flask
from flask import Blueprint

from flask_login import login_required

from app.decorators import admin_only
from app.utils.sites import site_map


# Import module forms
module = Blueprint("default", __name__)

@module.route("/")
@login_required
def home():
    return flask.render_template("home.html")

@module.route("/routes")
@login_required
def routes():
    links = site_map()
    links.extend(
        [
            # ("/api/v1/...", "blabla")
        ]
    )
    return flask.render_template("routes.html", links=links)
