import pandas as pd
from app.database.setup_postgres import PostgresConnection
from datetime import datetime

# Default datetime for NULL values
DEFAULT_DATETIME = datetime(1900, 1, 1)

def clean_dataframe(df):
    """
    Cleans the DataFrame by:
    1. Dropping the 'Unnamed: 0' column.
    2. Replacing missing values with default values.
    3. Ensuring datetime columns are properly formatted.
    4. Converting boolean columns to integers.
    """
    # Drop the 'Unnamed: 0' column if it exists
    if 'Unnamed: 0' in df.columns:
        df.drop(columns=['Unnamed: 0'], inplace=True)

    # Convert boolean columns to integers
    for col in ['Windows', 'Mac', 'Linux']:
        if col in df.columns:
            df[col] = df[col].astype(int, errors='ignore')  # Convert True -> 1, False -> 0

    # Replace missing values with defaults
    df.fillna({
        'AppID': 0,                     # BIGINT default
        'Name': '',                     # TEXT default
        'Release date': DEFAULT_DATETIME,  # TIMESTAMP default
        'Required age': 0,              # INT default
        'Price': 0.0,                   # DOUBLE PRECISION default
        'DLC count': 0,                 # INT default
        'About the game': '',           # TEXT default
        'Supported languages': '',      # TEXT default
        'Windows': -1,                  # SMALLINT (for boolean)
        'Mac': -1,                      # SMALLINT (for boolean)
        'Linux': -1,                    # SMALLINT (for boolean)
        'Positive': 0,                  # INT default
        'Negative': 0,                  # INT default
        'Score rank': 0.0,              # DOUBLE PRECISION default
        'Developers': '',               # TEXT default
        'Publishers': '',               # TEXT default
        'Categories': '',               # TEXT default
        'Genres': '',                   # TEXT default
        'Tags': ''                      # TEXT default
    }, inplace=True)

    # Convert 'Release date' to datetime
    if 'Release date' in df.columns:
        df['Release date'] = pd.to_datetime(df['Release date'], errors='coerce').fillna(DEFAULT_DATETIME)

    return df


def rename_columns_to_snake_case(df):
    """
    Renames DataFrame columns to snake_case for consistency with PostgreSQL schema.
    """
    rename_mapping = {
        'AppID': 'app_id',
        'Name': 'name',
        'Release date': 'release_date',
        'Required age': 'required_age',
        'Price': 'price',
        'DLC count': 'dlc_count',
        'About the game': 'about_the_game',
        'Supported languages': 'supported_languages',
        'Windows': 'windows',
        'Mac': 'mac',
        'Linux': 'linux',
        'Positive': 'positive',
        'Negative': 'negative',
        'Score rank': 'score_rank',
        'Developers': 'developers',
        'Publishers': 'publishers',
        'Categories': 'categories',
        'Genres': 'genres',
        'Tags': 'tags'
    }
    df.rename(columns=rename_mapping, inplace=True)
    return df


def write_dataframe_to_postgres(df, table_name='game_data'):
    """
    Writes the DataFrame to the PostgreSQL database.

    Args:
        df (pd.DataFrame): The DataFrame to insert into the database.
        table_name (str): The target table name in the PostgreSQL database.
    """
    conn = PostgresConnection.get_connection()
    cur = conn.cursor()

    # Prepare the data for insertion
    data_tuples = [tuple(row) for row in df.itertuples(index=False)]

    # Create the INSERT query dynamically based on column names
    columns = ', '.join(df.columns)
    placeholders = ', '.join(['%s'] * len(df.columns))
    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"

    try:
        cur.executemany(insert_query, data_tuples)
        conn.commit()
        print(f"Data written successfully to table '{table_name}'")
    except Exception as e:
        print(f"Error writing data to PostgreSQL: {e}")
        conn.rollback()
    finally:
        cur.close()


def query_data_from_postgres(params):

    # Define the columns in your database (19 columns in total)
    columns = [
        'app_id', 'name', 'release_date', 'required_age', 'price', 'dlc_count',
        'about_the_game', 'supported_languages', 'windows', 'mac', 'linux',
        'positive', 'negative', 'score_rank', 'developers', 'publishers',
        'categories', 'genres', 'tags'
    ]
    # Initialize the SQL query base
    base_query = "SELECT * FROM game_data WHERE TRUE"
    
    # List to hold query conditions
    conditions = []
    params_list = []  # List to collect values for safe parameterized queries
    
    # Handle each query parameter dynamically
    for field, value in params.items():
        if field in columns:  # Only handle parameters that correspond to the valid columns
            if field == "release_date":  # Exact match for release_date (date)
                conditions.append(f"release_date = %s")
                params_list.append(value)
            elif isinstance(value, str):  # Substring match for string columns
                conditions.append(f"{field} ILIKE %s")
                params_list.append(f"%{value}%")
            else:  # Exact match for numerical fields
                conditions.append(f"{field} = %s")
                params_list.append(value)
        # Handle special date filters like release_date__gte and release_date__lte
        elif field.startswith("release_date__gte"):  # Greater than or equal for date
            conditions.append("release_date >= %s")
            params_list.append(value)
        elif field.startswith("release_date__lte"):  # Less than or equal for date
            conditions.append("release_date <= %s")
            params_list.append(value)
    
    # Add the conditions to the base query
    if conditions:
        base_query += " AND " + " AND ".join(conditions)
    
    # Execute the query with parameters to prevent
    try:
        conn = PostgresConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute(base_query, params_list)  # Pass the params_list to execute
        rows = cursor.fetchall()
    
        # Format the result as a list of dictionaries
        columns = [desc[0] for desc in cursor.description]
        data = [dict(zip(columns, row)) for row in rows]
        cursor.close()
        return data
    except Exception as e:
        # Handle any errors during query execution
        print(f"Error executing query: {e}")
        return {"error": str(e)}


