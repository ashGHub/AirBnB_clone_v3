#!/usr/bin/python3
"""
Module for AirBnB clone place amenity api
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_amenities_by_place_id(place_id):
    """
    api route to get all place amenities for a given place id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    result = []
    for amenity in place.amenities:
        result.append(amenity.to_dict())
    return make_response(jsonify(result))


@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>',
    methods=['DELETE']
)
def delete_aminity(place_id, amenity_id):
    """
    endpoint to delete amenity by given place id and amenity id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    result = {}
    return make_response(jsonify(result), 200)


@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>',
    methods=['POST']
)
def add_aminity(place_id, amenity_id):
    """
    endpoint to add new amenity to a given place id and amenity id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return make_response(jsonify(amenity.to_dict()), 200)
    place.amenities.append(amenity)
    storage.save()
    result = amenity.to_dict()
    return make_response(jsonify(result), 201)
