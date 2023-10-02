#!/usr/bin/python3
"""
This script runs a  states view for the API
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """Retrieve list of all State objects"""
    state_objects = storage.all(State)
    state_dicts = [state.to_dict() for state in state_objects.values()]
    return jsonify(state_dicts)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def single_state(state_id):
    """Retrieve State object"""
    one_state = storage.get(State, state_id)
    if not one_state:
        abort(404)
    return jsonify(one_state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_state(state_id):
    """Delete a State object"""
    all_states = storage.get(State, state_id)
    if not all_states:
        abort(404)
    all_states.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Return the new created State with the status code 201"""
    new_state = request.get_json()
    if not new_state:
        abort(400, "Not a JSON")
    if 'name' not in new_state:
        abort(400, "Missing name")
    state = State(**new_state)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")

    for key, value in req.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    storage.save()
    return jsonify(state.to_dict()), 200
