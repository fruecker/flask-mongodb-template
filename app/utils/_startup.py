
import os

from flask_mongoengine import MongoEngine

def init_database(flask_app):
    """Initalize database connection to mongoengine"""

    # Set database connection details on flask app
    flask_app.config["MONGODB_SETTINGS"] = {
        "db" : f"{os.environ['DB_NAME']}",
        "host" : f"mongodb+srv://{os.environ['DB_USER']}:{os.environ['DB_PW']}@{os.environ['DB_CLUSTER']}.mongodb.net/{os.environ['DB_NAME']}?retryWrites=true&w=majority",
        "connect" : False
    }

    # Mount MongoEngine on flask application
    db = MongoEngine(flask_app)

    return db


def setup_directories():
    """Sets up central directories for access from other modules"""
    TEMPLATES_DIR = os.path.abspath("./app/templates")
    STATIC_DIR = os.path.abspath("./app/static")
    ROOT_DIR = os.path.abspath(".")
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        # In case of central templates folder
        # TEMPLATES_DIR = path.abspath('/templates')
        print("[INIT] TEMPLATE_DIR:", TEMPLATES_DIR)
        # Central static folder
        print("[INIT] STATIC_DIR:", STATIC_DIR)

    return TEMPLATES_DIR, STATIC_DIR, ROOT_DIR