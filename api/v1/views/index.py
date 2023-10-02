#!/usr/bin/python3
"""
Module for AirBnB clone index route
"""
from api.v1.views import app_views
from flask import jsonify, make_response


@app_views.route('/status')
def status():
    """
    Returns a JSON string with the status of the API
    """
    result = jsonify({'status': 'OK'})
    return make_response(result)
