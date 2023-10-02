#!/usr/bin/python3
'''places reviews'''
from api.v1.views import app_views
from flask import abort, request, jsonify, make_response
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def get_amenities_pl(place_id):
    ''' get all amenities in a place'''
    di = storage.get(Place, place_id)
    if not di:
        abort(404)
    amenities_list = []
    for amenity in di.amenities:
        di = amenity.to_dict()
        amenities_list.append(di)
    return jsonify(amenities_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_amenity_pl(place_id, amenity_id):
    '''DELETE method'''
    di = storage.get(Place, place_id)
    am = storage.get(Amenity, amenity_id)
    if not di or not am or am not in di.amenities:
        abort(404)
    di.amenities.remove(am)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenity(place_id, amenity_id):
    '''POST method'''
    di = storage.get(Place, place_id)
    am = storage.get(Amenity, amenity_id)
    if not di or not am or am not in di.amenities:
        abort(404)
    if am in di.amenities:
        return (jsonify(am.to_dict()), 200)
    if models.storage_t == 'db':
        di.amenities.append(am)
    else:
        di.amenity_ids.append(amenity_id)
    storage.save()
    return (jsonify(am.to_dict()), 201)
    content = request.get_json()
