#from .setup import setup_routes
# from .setup import setup_db_schema
from .upload_csv import upload_csv_route

def init_routes(app):
    # Register the setup and upload_csv routes
    # setup_db_schema(app)
    upload_csv_route(app)
