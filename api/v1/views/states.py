#!/usr/bin/python3
"""This module provides API endpoints for states"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_state_all():
    """retrieves all states in the storage"""
    state_all = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(state_all)


@app_views.route('states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """retrieves a state by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """deletes a state by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """creates a new state"""
    state = request.get_json()
    if not state:
        abort(400, "Not a JSON")
    if 'name' not in state.keys():
        abort(400, "Missing name")
    new_state = State(**state)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """updates a state in the storage"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    s = request.get_json()
    if not s:
        abort(400, "Not a JSON")
    for key, val in s.items():
        if key in ['id', 'created_at', 'updated_at']:
            pass
        else:
            setattr(state, key, val)
    storage.save()
    return jsonify(state.to_dict()), 200
