#!/usr/bin/python3
"""
Module for AirBnB clone places api
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """
    endpoint to get all places for a given city id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    result = []
    for city in city.places:
        result.append(city.to_dict())
    return make_response(jsonify(result))


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place_by_id(place_id):
    """
    endpoint to get place by given place id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    result = place.to_dict()
    return make_response(jsonify(result))


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """
    endpoint to delete place by given place id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    result = {}
    return make_response(jsonify(result), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def add_place_for_city(city_id):
    """
    endpoint to add new place to a given city id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    if 'user_id' not in body:
        abort(400, "Missing user_id")
    user = storage.get(User, body['user_id'])
    if user is None:
        abort(404)
    if 'name' not in body:
        abort(400, "Missing name")
    place = Place(city_id=city_id, **body)
    storage.new(place)
    storage.save()
    result = place.to_dict()
    return make_response(jsonify(result), 201)


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """
    endpoint to update a place for given place id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    for key, value in body.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    result = place.to_dict()
    return make_response(jsonify(result), 200)


@app_views.route('/places_search', methods=['POST'])
def search_places():
    """
    endpoint to search places for given states, cities, and amenities
    """
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    states = body['states'] if 'states' in body else None
    cities = body['cities'] if 'cities' in body else None
    amenities = body['amenities'] if 'amenities' in body else None
    pl = storage.all(Place).values()
    if states:
        pl = [p for p in pl if p.city.state_id in states]
    if cities:
        pl = [p for p in pl if p.city_id in cities]
    if amenities:
        pl = [p for p in pl if all(am in p.amenities for am in amenities)]
    result = []
    for p in pl:
        result.append(p.to_dict())
    return make_response(jsonify(result), 200)
