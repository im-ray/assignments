from flask import request, jsonify
from app.database.postgres_helper import query_data_from_postgres

def data_explorer_route(app):
    @app.route('/data_explorer', methods=['GET'])
    def data_explorer():
        # Extract query parameters
        params = request.args.to_dict()
        
        try:
            # Call the function to query data based on parameters
            data = query_data_from_postgres(params)
            
            # Return the result as JSON
            return jsonify(data), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
