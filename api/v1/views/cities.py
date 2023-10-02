#!/usr/bin/python3
"""This module provides API endpoints for cities"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """retrieves all cities in a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def place_by_id(place_id):
    """retrieves a place by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """deletes a city by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """creates a new city"""
    state = storage.get(State, state_id)
    if not state:
        abort(400)
    city = request.get_json()
    if not city:
        abort(400, "Not a JSON")
    if 'name' not in city.keys():
        abort(400, "Missing name")
    new_city = City(**city)
    setattr(new_city, 'state_id', state_id)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """updates a city in the storage"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    c = request.get_json()
    if not c:
        abort(400, "Not a JSON")
    for key, val in c.items():
        if key in ['id', 'state_id', 'created_at', 'updated_at']:
            pass
        else:
            setattr(city, key, val)
    storage.save()
    return jsonify(city.to_dict()), 200
