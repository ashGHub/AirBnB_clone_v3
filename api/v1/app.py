#!/usr/bin/python3
"""
Module for AirBnB clone startup api
Mainly contains app entry point and cross concerns
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from models import storage
from os import getenv


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    Teardown appcontext to be called on every request
    This will remove the current SQLAlchemy Session
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """
    404 page not found handler
    """
    result = jsonify({'error': 'Not found'})
    return make_response(result, 404)


if __name__ == "__main__":
    """
    App entry point for AirBnB clone startup api
    """
    host = getenv("HBNB_API_HOST", default="0.0.0.0")
    port = getenv("HBNB_API_PORT", default=5000)
    app.run(host=host, port=port, threaded=True)
