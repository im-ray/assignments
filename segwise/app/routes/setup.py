from flask import jsonify
# from ..database import create_database_and_table
from ..database import get_client

# def setup_routes(app):
#     @app.route('/setup', methods=['GET'])
    
#     def setup_db_schema():
#         client = get_client()
#         result = create_database_and_table()
#         return jsonify({'message': result})

# from flask import jsonify
# from ..database import get_client

def setup_db_schema():
    """This function is called to set up the database schema directly."""
    client = get_client()

    try:
        # Create the database if it doesn't exist
        client.execute('CREATE DATABASE IF NOT EXISTS analytics')

        # Create the table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS analytics.game_data (
            app_id Int64,
            name String,
            release_date DateTime,
            required_age Int64,
            price Float64,
            dlc_count Int64,
            about_the_game String,
            supported_languages String,
            windows UInt8,
            mac UInt8,
            linux UInt8,
            positive Int64,
            negative Int64,
            score_rank Float64,
            developers String,
            publishers String,
            categories String,
            genres String,
            tags String
        ) ENGINE = MergeTree()
        ORDER BY release_date;
        """
        
        # Execute the table creation query
        client.execute(create_table_query)
        print("Database and table created successfully!")  # Logging for confirmation

    except Exception as e:
        print(f"Error setting up database: {str(e)}")
        return jsonify({'error': f'Error setting up database: {str(e)}'}), 500








# def setup_db_schema(app):
#     # Ensure this decorator is applied to the app after it has been created
#     """This function will be called when the app is created"""
#     @app.before_first_request
#     def setup():
#         """Called only once when the app first starts"""
#         client = get_client()
        
#         try:
#             # Create the database if it doesn't exist
#             client.execute('CREATE DATABASE IF NOT EXISTS analytics')

#             # Create the table if it doesn't exist
#             create_table_query = """
#             CREATE TABLE IF NOT EXISTS analytics.game_data (
#                 app_id Int64,
#                 name String,
#                 release_date DateTime,
#                 required_age Int64,
#                 price Float64,
#                 dlc_count Int64,
#                 about_the_game String,
#                 supported_languages String,
#                 windows UInt8,
#                 mac UInt8,
#                 linux UInt8,
#                 positive Int64,
#                 negative Int64,
#                 score_rank Float64,
#                 developers String,
#                 publishers String,
#                 categories String,
#                 genres String,
#                 tags String
#             ) ENGINE = MergeTree()
#             ORDER BY release_date;
#             """
            
#             # Execute the table creation query
#             client.execute(create_table_query)
#             # return jsonify({'message': 'Database and table created successfully!'})
#             print("Database and table created successfully!")  # Logging for confirmation

#         except Exception as e:
#             print(f"Error setting up database and table: {str(e)}")
#             return jsonify({'error': f'Error setting up database: {str(e)}'}), 500
#             # return jsonify({'error': str(e)}), 500