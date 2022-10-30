
from functools import wraps
import flask

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