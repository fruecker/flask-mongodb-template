
from functools import wraps
import flask
import os

from flask_login import current_user

def admin_only(function):
    """Decorate a function with this decorator to make sure that only admin users are allowed 
    to access."""

    @wraps(function)
    def admin_only_function(*args, **kwargs):
        if not current_user.is_admin():
            err = "Du bist kein Admin."
            flask.flash(err, "danger")
            return flask.redirect(flask.url_for("default.home"))
        return function(*args, **kwargs)

    return admin_only_function


def cronjob(function):
    """Decorate a funtion with this decorator to check before executing wheather a paramater 'verification'
    was sent with the app secret."""

    @wraps(function)
    def cronjob_function(*args, **kwargs):
        if not flask.request.args.get('verification', type=str) == os.environ.get('APP_SECRET'):
            return 'Invalid verification key!', 403
        return function(*args, **kwargs)

    return cronjob_function


def under_construction(function):
    """Decorate a function with this decorator to redirect to the 'under construction' page."""

    @wraps(function)
    def under_construction_function(*args, **kwargs):
        return flask.render_template("under_construction.html")

    return under_construction_function