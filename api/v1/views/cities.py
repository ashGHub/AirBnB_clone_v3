#!/usr/bin/python3
"""
Module for AirBnB clone cities api
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities_by_state_id(state_id):
    """
    endpoint to get all cities for a given state id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    result = []
    for city in state.cities:
        result.append(city.to_dict())
    return make_response(jsonify(result))


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city_by_id(city_id):
    """
    endpoint to get city by given city id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    result = city.to_dict()
    return make_response(jsonify(result))


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """
    endpoint to delete city by given city id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    result = {}
    return make_response(jsonify(result), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def add_city_for_state(state_id):
    """
    endpoint to add new city to a given state id
    """
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    if 'name' not in body:
        abort(400, "Missing name")
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city = City(state_id=state_id, **body)
    storage.new(city)
    storage.save()
    result = city.to_dict()
    return make_response(jsonify(result), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """
    endpoint to update a city for given city id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    for key, value in body.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    result = city.to_dict()
    return make_response(jsonify(result), 200)
