#!/usr/bin/python3
"""This module provides API endpoints for reviews"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """retrieves all reviews for a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def review_by_id(review_id):
    """retrieves a review by id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """deletes a review by id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """creates a new review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(400)
    review = request.get_json()
    if not review:
        abort(400, "Not a JSON")
    if 'user_id' not in review.keys():
        abort(400, "Missing user_id")
    user = storage.get(User, review['user_id'])
    if not user:
        abort(404)
    if 'text' not in review:
        abort(400, "Missing text")
    new_review = Review(**review)
    setattr(new_review, 'place_id', place_id)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """updates a review for a place"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    r = request.get_json()
    if not r:
        abort(400, "Not a JSON")
    for key, val in r.items():
        if key in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            pass
        else:
            setattr(review, key, val)
    storage.save()
    return jsonify(review.to_dict()), 200
