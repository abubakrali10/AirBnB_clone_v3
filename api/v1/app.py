#!/usr/bin/python3
"""The flask app"""
import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def t_down(exception):
    """handles the app teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """handles page not found error"""
    err = {
        "error": "Not found"
    }
    return jsonify(err), 404


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST")
    port = int(os.getenv("HBNB_API_PORT"))
    app.run(host=host, port=port, threaded=True)
