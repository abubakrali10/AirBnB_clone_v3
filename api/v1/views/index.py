from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def api_status():
    """returns api status"""
    status = {"status": "OK"}
    return jsonify(status)
