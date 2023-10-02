#!/usr/bin/python3
"""This module provides API endpoints for amenities"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities_all():
    """retrieves list of all Amenity"""
    amenities = [ame.to_dict() for ame in storage.all(Amenity).values()]
    return jsonify(amenities)


@app_views.route('amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def amenity_by_id(amenity_id):
    """retrieves an amenity using id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes an amenity using id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """creates a new amenity"""
    amenity = request.get_json()
    if not amenity:
        abort(400, "Not a JSON")
    if 'name' not in amenity.keys():
        abort(400, "Missing name")
    new_amenity = Amenity(**amenity)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict())


@app_views.route('amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """updates an existing amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    a = request.get_json()
    if not a:
        abort(400, "Not a JSON")
    for key, val in a.items():
        if key in ['id', 'created_at', 'updated_at']:
            pass
        else:
            setattr(amenity, key, val)
    storage.save()
    return jsonify(amenity.to_dict()), 200
