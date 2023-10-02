#!/usr/bin/python3
'''flask main app'''
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(down_with_the_base):
    '''teardown function'''
    storage.close()


@app.errorhandler(404)
def handle_api_error(e):
    '''status code 404 handler'''
    return(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    app.run(host=getenv("HBNB_API_HOST", '0.0.0.0'),
            port=getenv("HBNB_API_PORT", '5000'), threaded=True)
