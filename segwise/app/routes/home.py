from flask import render_template
from flask import Flask

def home_route(app):
    @app.route('/')
    def home():
        # Render the HTML page
        return render_template('index.html')
