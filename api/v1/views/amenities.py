#!/usr/bin/python3
'''amenities'''
from api.v1.views import app_views
from flask import abort, request, jsonify, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenities(amenity_id=None):
    '''get all amenities or a specific amenity by id'''
    if not amenity_id:
        amenities_list = []
        for state in storage.all(Amenity).values():
            di = state.to_dict()
            amenities_list.append(di)
        return jsonify(amenities_list)
    else:
        di = storage.get(Amenity, amenity_id)
        if di:
            return jsonify(di.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_amenity(amenity_id):
    '''DELETE method'''
    di = storage.get(Amenity, amenity_id)
    if not di:
        abort(404)
    storage.delete(di)
    storage.save()
    return jsonify({})  # check content/type


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    '''POST method'''
    content = request.get_json()
    if not content:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in content:
        return make_response(jsonify({"error": "Missing name"}), 400)
    st = Amenity(**content)
    storage.new(st)
    storage.save()
    return (jsonify(st.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    '''PUT method for amenities'''
    di = storage.get(Amenity, amenity_id)
    if not di:
        abort(404)
    content = request.get_json()
    if not content:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for k, v in content.items():
        if k not in ['id', 'created_at', 'updated']:
            setattr(di, k, v)
    storage.save()
    return jsonify(di.to_dict())
