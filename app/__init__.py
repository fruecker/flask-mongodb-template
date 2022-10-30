
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
    injections = dict()
    return injections

# Import modules (blueprints)
from app.modules.default.views import module_default as blueprint_default

# Register those modules
app.register_blueprint(blueprint_default, static_url_path=STATIC_DIR, template_folder=TEMPLATES_DIR)
