#!/usr/bin/python3
"""This module provides API endpoints for users"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users_all():
    """retrieves list of all users"""
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def user_by_id(user_id):
    """retrieves a user using id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """deletes a user using id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """creates a new user"""
    user = request.get_json()
    if not user:
        abort(400, "Not a JSON")
    if 'email' not in user.keys():
        abort(400, "Missing email")
    if 'password' not in user.keys():
        abort(400, "Missing password")
    new_user = User(**user)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict())


@app_views.route('users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """updates an existing user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    u = request.get_json()
    if not u:
        abort(400, "Not a JSON")
    for key, val in u.items():
        if key in ['id', 'email', 'created_at', 'updated_at']:
            pass
        else:
            setattr(user, key, val)
    storage.save()
    return jsonify(user.to_dict()), 200
