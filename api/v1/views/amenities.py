#!/usr/bin/python3
"""
Module for AirBnB clone amenities api
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    """
    endpoint to get all amenities
    """
    result = []
    for amenity in storage.all(Amenity).values():
        result.append(amenity.to_dict())
    return make_response(jsonify(result))


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity_by_id(amenity_id):
    """
    endpoint to get amenity by given amenity id
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    result = amenity.to_dict()
    return make_response(jsonify(result))


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """
    endpoint to delete amenity by given amenity id
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    result = {}
    return make_response(jsonify(result), 200)


@app_views.route('/amenities', methods=['POST'])
def add_amenity():
    """
    endpoint to add new amenity
    """
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    if 'name' not in body:
        abort(400, "Missing name")
    amenity = Amenity(**body)
    storage.new(amenity)
    storage.save()
    result = amenity.to_dict()
    return make_response(jsonify(result), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """
    endpoint to update a amenity for given amenity id
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    for key, value in body.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    result = amenity.to_dict()
    return make_response(jsonify(result), 200)
