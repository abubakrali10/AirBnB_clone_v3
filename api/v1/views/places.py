#!/usr/bin/python3
"""This module provides API endpoints for cities"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """retrieves all places in a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def place_by_id(place_id):
    """retrieves a place by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """deletes a place by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """creates a new place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    place = request.get_json()
    if not place:
        abort(400, "Not a JSON")
    if 'user_id' not in place.keys():
        abort(400, "Missing user_id")
    user = storage.get(User, place['user_id'])
    if not user:
        abort(404)
    if 'name' not in place.keys():
        abort(400, "Missing name")
    new_place = Place(**place)
    setattr(new_place, 'city_id', city_id)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """updates a place in the storage"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    p = request.get_json()
    if not p:
        abort(400, "Not a JSON")
    for key, val in p.items():
        if key in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            pass
        else:
            setattr(place, key, val)
    storage.save()
    return jsonify(place.to_dict()), 200
