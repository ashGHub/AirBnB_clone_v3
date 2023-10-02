#!/usr/bin/python3
"""
Module for AirBnB clone index route
"""
from api.v1.views import app_views
from flask import jsonify, make_response
from models import storage


@app_views.route('/status')
def status():
    """
    Returns a JSON string with the status of the API
    """
    result = jsonify({'status': 'OK'})
    return make_response(result)


@app_views.route('/stats')
def stats():
    """
    Returns stats for each class
    """
    result = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return make_response(jsonify(result))
