#!/usr/bin/python3
"""
module to create routes for API
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def api_status():
    """returns api status"""
    status = {"status": "OK"}
    return jsonify(status)
