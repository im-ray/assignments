import psycopg2
from psycopg2 import sql
from config import PostgresConfig

class PostgresConnection:
    """
    Singleton class to handle the PostgreSQL connection.
    Ensures that only one connection is created and reused across the app.
    """
    _connection = None

    @staticmethod
    def get_connection():
        """
        Returns the PostgreSQL connection. If the connection doesn't exist, it creates one.
        """
        if PostgresConnection._connection is None:
            PostgresConnection._connection = psycopg2.connect(PostgresConfig.get_connection_string())
        return PostgresConnection._connection

    @staticmethod
    def close_connection():
        """
        Closes the PostgreSQL connection.
        """
        if PostgresConnection._connection:
            PostgresConnection._connection.close()
            PostgresConnection._connection = None


def create_table_if_not_exists():
    """
    Creates the necessary tables in the PostgreSQL database if they do not exist.
    """
    conn = PostgresConnection.get_connection()
    cur = conn.cursor()

    # SQL query to create table (if not exists)
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS game_data (
        app_id BIGINT DEFAULT 0,
        name TEXT DEFAULT '',
        release_date TIMESTAMP DEFAULT '1900-01-01 00:00:00',
        required_age INT DEFAULT 0,
        price DOUBLE PRECISION DEFAULT 0.0,
        dlc_count INT DEFAULT 0,
        about_the_game TEXT DEFAULT '',
        supported_languages TEXT DEFAULT '',
        windows SMALLINT DEFAULT -1,
        mac SMALLINT DEFAULT -1,
        linux SMALLINT DEFAULT -1,
        positive INT DEFAULT 0,
        negative INT DEFAULT 0,
        score_rank DOUBLE PRECISION DEFAULT 0.0,
        developers TEXT DEFAULT '',
        publishers TEXT DEFAULT '',
        categories TEXT DEFAULT '',
        genres TEXT DEFAULT '',
        tags TEXT DEFAULT ''
    );
    '''

    try:
        # Execute the query
        cur.execute(create_table_query)
        conn.commit()
        print("Table created (if not exists) successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")
        conn.rollback()
    finally:
        # Close the cursor (no need to close the connection as it's reused)
        cur.close()


# If you want to ensure the connection is created once and reused, call this function when the app starts
# if __name__ == "__main__":
#     create_table_if_not_exists()
