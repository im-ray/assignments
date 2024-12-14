from flask import Flask
from .routes import init_routes
from .routes.setup import setup_db_schema

def create_app():
    app = Flask(__name__)

    # Directly call the setup_db_schema function
    setup_db_schema()
    # Register routes
    init_routes(app)

    return app
