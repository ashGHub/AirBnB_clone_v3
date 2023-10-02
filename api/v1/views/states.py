#!/usr/bin/python3
"""
Module for AirBnB clone states api
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_states():
    """
    endpoint to get all states
    """
    result = []
    for state in storage.all(State).values():
        result.append(state.to_dict())
    return make_response(jsonify(result))


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state_by_id(state_id):
    """
    endpoint to get state by given state id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    result = state.to_dict()
    return make_response(jsonify(result))


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """
    endpoint to delete state by given state id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    result = {}
    return make_response(jsonify(result), 200)


@app_views.route('/states', methods=['POST'])
def add_state():
    """
    endpoint to add new state
    """
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    if 'name' not in body:
        abort(400, "Missing name")
    state = State(**body)
    storage.new(state)
    storage.save()
    result = state.to_dict()
    return make_response(jsonify(result), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """
    endpoint to update state by given state id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    for key, value in body.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    result = state.to_dict()
    return make_response(jsonify(result), 200)
