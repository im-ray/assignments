from flask import Flask
from .routes import init_routes
# from .routes.setup import setup_db_schema
from app.database.setup_postgres import create_table_if_not_exists

def create_app():
    app = Flask(__name__)

    # Directly call the setup_db_schema function
    # setup_db_schema()
    # Setup the PostgreSQL table (using the shared connection)
    create_table_if_not_exists()
    # Register routes
    init_routes(app)

    return app
