#!/usr/bin/python3
"""
Module for AirBnB clone users api
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def get_users():
    """
    endpoint to get all users
    """
    result = []
    for user in storage.all(User).values():
        result.append(user.to_dict())
    return make_response(jsonify(result))


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """
    endpoint to get user by given user id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    result = user.to_dict()
    return make_response(jsonify(result))


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    """
    endpoint to delete user by given user id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    result = {}
    return make_response(jsonify(result), 200)


@app_views.route('/users', methods=['POST'])
def add_user():
    """
    endpoint to add new user
    """
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    if 'email' not in body:
        abort(400, "Missing email")
    if 'password' not in body:
        abort(400, "Missing password")
    user = User(**body)
    storage.new(user)
    storage.save()
    result = user.to_dict()
    return make_response(jsonify(result), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    endpoint to update a user for given user id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    for key, value in body.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    result = user.to_dict()
    return make_response(jsonify(result), 200)
