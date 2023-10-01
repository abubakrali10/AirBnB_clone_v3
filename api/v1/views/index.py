#!/usr/bin/python3
"""
module to create routes for API
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


classes = {"amenities": "Amenity", "cities": "City",
           "places": "Place", "reviews": "Review",
           "states": "State", "users": "User"}


@app_views.route('/status')
def api_status():
    """returns api status"""
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route('stats')
def app_stats():
    """retrieving statistics of different objects"""
    stats = {}
    for k, v in classes.items():
        stats[k] = storage.count(v)
    return jsonify(stats)
