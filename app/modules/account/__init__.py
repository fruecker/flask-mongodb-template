import flask_login
import flask_bcrypt
from app.database.models.user import User

from app import app

# Setup login manager
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "account.login"
login_manager.login_message = "Bitte logge dich ein."
login_manager.login_message_category = "info"
login_manager.refresh_view = "account.login"
login_manager.needs_refresh_message = "Bitte logge dich erneut ein."
login_manager.needs_refresh_message_category = "info"
# login_manager.session_protection = "strong"

# Login Manager callbacks
@login_manager.user_loader
def load_user(user_id):
    """This function specifies how to load a user"""
    return User.load(email=user_id)


# Bcrypt
bcrypt = flask_bcrypt.Bcrypt(app)