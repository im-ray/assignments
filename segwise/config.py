class Config:
    CLICKHOUSE_HOST = 'localhost'
    CLICKHOUSE_USER = 'rupesh'
    CLICKHOUSE_PASSWORD = 'Rupesh123'


class PostgresConfig:
    """
    PostgreSQL configuration class that contains the necessary connection details.
    """
    # Database connection details
    POSTGRES_HOST = 'localhost'  # Use 'localhost' for Docker setup
    POSTGRES_USER = 'postgres'
    POSTGRES_PASSWORD = 'postgres'
    POSTGRES_DB = 'analytics'
    POSTGRES_PORT = 5432  # Default PostgreSQL port

    @staticmethod
    def get_connection_string():
        """
        Returns the connection string used by psycopg2 to connect to the database.
        """
        return f"postgresql://{PostgresConfig.POSTGRES_USER}:{PostgresConfig.POSTGRES_PASSWORD}@" \
               f"{PostgresConfig.POSTGRES_HOST}:{PostgresConfig.POSTGRES_PORT}/{PostgresConfig.POSTGRES_DB}"
