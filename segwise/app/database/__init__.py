from clickhouse_driver import Client
from config import Config

# Set up the ClickHouse client
# client = Client(host='localhost', user='rupesh', password='Rupesh123')

# Set up ClickHouse client connection
client = Client(
    host=Config.CLICKHOUSE_HOST,
    user=Config.CLICKHOUSE_USER,
    password=Config.CLICKHOUSE_PASSWORD
)

def get_client():
    return client


# def create_database_and_table():
#     try:
#         # Create the database if it doesn't exist
#         client.execute('CREATE DATABASE IF NOT EXISTS analytics')

#         # Create the table if it doesn't exist
#         create_table_query = """
#         CREATE TABLE IF NOT EXISTS analytics.game_data (
#             app_id Int64,
#             name String,
#             release_date DateTime,
#             required_age Int64,
#             price Float64,
#             dlc_count Int64,
#             about_the_game String,
#             supported_languages String,
#             windows UInt8,
#             mac UInt8,
#             linux UInt8,
#             positive Int64,
#             negative Int64,
#             score_rank Float64,
#             developers String,
#             publishers String,
#             categories String,
#             genres String,
#             tags String
#         ) ENGINE = MergeTree()
#         ORDER BY release_date;
#         """

#         # Execute the table creation query
#         client.execute(create_table_query)

#         return "Database and table created successfully!"
    
#     except Exception as e:
#         return f"Error: {str(e)}"


# in clickhouse Type bool is internally stored as UInt8, true (1), false (0).

