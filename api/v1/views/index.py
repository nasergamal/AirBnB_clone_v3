#!/usr/bin/python3
'''status and stats of objects'''
from api.v1.views import app_views
from flask import jsonify
from models.engine.db_storage import classes
from models import storage


@app_views.route('/status')
def status():
    '''Return ok '''
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stat():
    '''return count of all objects'''
    objs = {"amenities": "Amenity", "cities": "City", "places": "Place",
            "reviews": "Review", "states": "State", "users": "User"}
    s = {k: storage.count(v) for k, v in objs.items()}
    return(jsonify(s))
