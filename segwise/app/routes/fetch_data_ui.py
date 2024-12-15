from flask import render_template

def fetch_data_ui(app):
    @app.route('/fetch_data', methods=['GET'])
    def data_explorer_ui():
        return render_template('data_explorer.html')  # The template for the UI