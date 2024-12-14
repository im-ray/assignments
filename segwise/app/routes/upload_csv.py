from flask import request, jsonify
import pandas as pd
from ..database import get_client

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
