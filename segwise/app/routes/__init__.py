#from .setup import setup_routes
# from .setup import setup_db_schema
# from .upload_csv import upload_csv_route, upload_csv_with_url
from .upload_csv import upload_csv_with_url
from .home import home_route
from .data_explorer import data_explorer_route

def init_routes(app):
    # Register the setup and upload_csv routes
    # setup_db_schema(app)
    # upload_csv_route(app=app)
    home_route(app)
    upload_csv_with_url(app=app)
    data_explorer_route(app)
