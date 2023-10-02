#!/usr/bin/python3
"""
Module for AirBnB clone reviews api
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews_by_place_id(place_id):
    """
    api route to get all reviews for a given place id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    result = []
    for review in place.reviews:
        result.append(review.to_dict())
    return make_response(jsonify(result))


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review_by_id(review_id):
    """
    endpoint to get review by given review id
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    result = review.to_dict()
    return make_response(jsonify(result))


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """
    endpoint to delete review by given review id
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    result = {}
    return make_response(jsonify(result), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def add_review_for_place(place_id):
    """
    endpoint to add new review to a given place id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    if 'user_id' not in body:
        abort(400, "Missing user_id")
    user = storage.get(User, body['user_id'])
    if user is None:
        abort(404)
    if 'text' not in body:
        abort(400, "Missing text")
    review = Review(place_id=place_id, **body)
    storage.new(review)
    storage.save()
    result = review.to_dict()
    return make_response(jsonify(result), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """
    endpoint to update a review for given review id
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    for key, value in body.items():
        exludes = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        if key not in exludes:
            setattr(review, key, value)
    storage.save()
    result = review.to_dict()
    return make_response(jsonify(result), 200)
