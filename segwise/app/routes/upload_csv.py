from flask import request, jsonify
import pandas as pd
from ..database import get_client

def upload_csv_with_url(app):
    @app.route('/upload_csv_url', methods=['POST'])
    def upload_csv_from_url():
        # Ensure a URL is provided in the request
        data = request.get_json()
        if 'csv_url' not in data:
            return jsonify({'error': 'No csv_url provided'}), 400

        csv_url = data['csv_url']

        try:
            # Step 1: Read the CSV file from the provided URL
            df = read_csv_from_url(csv_url)

            # Step 2: Map DataFrame to ClickHouse schema
            df_mapped = map_df_to_schema(df)

            # Step 3: Handle missing values in the DataFrame
            df_cleaned = handle_missing_values(df_mapped)

            # Step 4: Insert data into ClickHouse
            insert_data_to_clickhouse(df_cleaned)

            return jsonify({'message': 'CSV data processed and uploaded successfully'}), 200

        except Exception as e:
            return jsonify({'error': f'Failed to process file: {str(e)}'}), 500

def upload_csv_route(app):
    @app.route('/upload_csv', methods=['POST'])
    def upload_csv():
        # Ensure a file is provided in the request
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        # Check if a file is selected
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        try:
            # Read the CSV file using pandas
            df = pd.read_csv(file)

            # Drop 'Unnamed: 0' column in place (because it's an index
            df.drop(columns=['Unnamed: 0'], inplace=True, errors='ignore')


            # Rename relevant columns in one go
            df.rename(columns={
                'Release date': 'release_date',
                'Windows': 'windows',
                'Mac': 'mac',
                'Linux': 'linux',
                'Score rank': 'score_rank'
            }, inplace=True)

            # Rename 'Release date' column to 'release_date' in place
            # df.rename(columns={'Release date': 'release_date'}, inplace=True)

            # Convert 'release_date' to datetime
            df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')  
            # Use 'coerce' to handle invalid date formats

            # Convert boolean columns to int (0 or 1)
            # df.rename(columns={'Windows': 'windows'}, inplace=True)
            df['windows'] = df['windows'].astype(int)

            # df.rename(columns={'Mac': 'mac'}, inplace=True)
            df['mac'] = df['mac'].astype(int)

            # df.rename(columns={'Linux': 'linux'}, inplace=True)
            df['linux'] = df['linux'].astype(int)

            # Handle NaN values in 'Score rank' by replacing them with None (ClickHouse NULL)
            # df.rename(columns={'Score rank': 'score_rank'}, inplace=True)
            df['score_rank'] = df['score_rank'].fillna(None)

            # Insert data into ClickHouse
            insert_data_to_clickhouse(df)

            return jsonify({'message': 'CSV data uploaded successfully'}), 200

        except Exception as e:
            return jsonify({'error': f'Failed to process file: {str(e)}'}), 500

def insert_data_to_clickhouse(df):
    client = get_client()

    # Convert DataFrame to a list of dictionaries (records)
    data = df.to_dict('records')

    # Insert data into the 'game_data' table in ClickHouse
    client.execute('''
        INSERT INTO analytics.game_data (app_id, name, release_date, required_age, price, dlc_count, about_the_game, supported_languages, windows, mac, linux, positive, negative, score_rank, developers, publishers, categories, genres, tags) VALUES
    ''', data)


def read_csv_from_url(csv_url):
    """
    Reads a CSV file from the provided URL and returns a pandas DataFrame.

    Args:
        csv_url (str): URL of the CSV file to fetch.
    
    Returns:
        pd.DataFrame: DataFrame containing the CSV data.
    
    Raises:
        requests.exceptions.RequestException: If there's an error fetching the URL.
        ValueError: If the fetched content cannot be parsed into a DataFrame.
        for example: 
            invalid_csv: "https://github.com/im-ray/assignments/blob/main/segwise/game_data.csv"
            valid_csv : "https://raw.githubusercontent.com/im-ray/assignments/main/segwise/game_data.csv"

    """
    try:
        # Try reading the CSV from the URL
        df = pd.read_csv(csv_url)
        print("CSV file fetched and DataFrame created successfully!")
        return df
    
    except Exception as e:
        # Handle exceptions such as invalid URL, malformed CSV, etc.
        print(f"Error reading CSV from URL: {e}")
        return None  # Return None in case of an error


def map_df_to_schema(df):
    """
    Maps the DataFrame columns to match the schema of the ClickHouse 'game_data' table.

    Args:
        df (pd.DataFrame): The DataFrame to map to the schema.
    
    Returns:
        pd.DataFrame: The DataFrame with columns renamed, missing values handled, and types converted.
    """
    # Step 1: Drop 'Unnamed: 0' column if it exists (index column)
    df.drop(columns=['Unnamed: 0'], inplace=True, errors='ignore')

    # Step 2: Rename columns to match the ClickHouse schema
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

    # Step 3: Convert 'release_date' to datetime
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

    # Step 4: Convert boolean columns to integers (0 or 1)
    for col in ['windows', 'mac', 'linux']:
        if col in df.columns:
            df[col] = df[col].astype(int, errors='ignore')
    # Return the mapped DataFrame
    return df

def handle_missing_values(df):
    """
    Handles missing values for different data types in the DataFrame and replaces them with appropriate defaults.
    
    Args:
        df (pd.DataFrame): The DataFrame with potential missing values.
    
    Returns:
        pd.DataFrame: The DataFrame with missing values filled with default values.
    """
    # Handle String Columns (e.g., 'tags', 'developers')
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].fillna('').astype(str)  # Replace NaN with empty string and ensure it's string type

    # Handle Numeric Columns (e.g., 'price', 'dlc_count')
    for col in df.select_dtypes(include=['float64', 'int64']).columns:
        if df[col].dtype == 'float64':
            df[col] = df[col].fillna(0.0)  # Replace NaN with 0.0 for float columns (or use None for NULL)
        elif df[col].dtype == 'int64':
            df[col] = df[col].fillna(0)  # Replace NaN with 0 for integer columns

    # Handle Boolean Columns (e.g., 'windows', 'mac', 'linux')
    for col in df.select_dtypes(include=['bool']).columns:
        df[col] = df[col].fillna(False).astype(int)  # Replace NaN with False (0) for boolean columns and cast to int

    # Handle Datetime Columns (e.g., 'release_date')
    for col in df.select_dtypes(include=['datetime64']).columns:
        df[col] = df[col].fillna(pd.to_datetime('1970-01-01'))  # Replace NaT with a default date (e.g., '1970-01-01')

    return df


