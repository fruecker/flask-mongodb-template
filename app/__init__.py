
import os
import secrets

from flask_talisman import Talisman

from flask import Flask
from dotenv import load_dotenv

from app.utils._startup import init_database, setup_directories

# Try to load env vars from different places
if not load_dotenv():
    raise ValueError("Could not load environment variables... Make sure to provide a '.env' file")

# Define the WSGI application object
app = Flask(__name__)
app.secret_key = os.environ.get("APP_SECRET", secrets.token_urlsafe(16))

# Initialize the database
db = init_database(app)

# Initialize security settings
Talisman(app, content_security_policy=None)

# Declare default template and static directories for access from other modules
TEMPLATES_DIR, STATIC_DIR, ROOT_DIR = setup_directories()

# Context processor for injections to templates
# https://flask.palletsprojects.com/en/2.0.x/templating/#context-processors
@app.context_processor
def inject_template_scope():
    injections = dict(
        # injected_var_name =os.environ.get('injected_var_name', 'default_value'),
        )
    return injections

@app.template_filter('text_datetime')
def format_datetime(value, format="%d.%m.%Y %H:%M"):
    return value.strftime(format)

# Import modules (blueprints)
from app.modules.default.views import module as blueprint_default
from app.modules.account.views import module as blueprint_account
from app.modules.admin.views import module as blueprint_admin
from app.modules.api.v1.endpoints import module_api_v1 as blueprint_api_v1

# Register those modules
app.register_blueprint(blueprint_default, static_url_path=STATIC_DIR, template_folder=TEMPLATES_DIR)
app.register_blueprint(blueprint_account, static_url_path=STATIC_DIR, template_folder=TEMPLATES_DIR)
app.register_blueprint(blueprint_admin, static_url_path=STATIC_DIR, template_folder=TEMPLATES_DIR)
app.register_blueprint(blueprint_api_v1)