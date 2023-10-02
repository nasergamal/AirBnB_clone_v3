#!/usr/bin/python3
"""
This script Desribes the places view for the API
"""
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


@app_views.route('cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def place_city(city_id):
    """Retrieves the list of all Place objects of a City"""
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)

    return jsonify([city.to_dict() for city in city_obj.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def single_place(place_id):
    """Retrieves a Place from the DB"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_place(place_id):
    """deletes and returns an empty dictionary with the status code 200"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """creates and returns the new Place with the status code 201"""
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)

    new_place = request.get_json()
    if not new_place:
        abort(400, 'Not a JSON')
    if 'user_id' not in new_place:
        abort(400, "Missing user_id")
    user_id = new_place['user_id']
    obj_user = storage.get(User, user_id)
    if not obj_user:
        abort(404)
    if 'name' not in new_place:
        abort(400, "Missing name")

    city_obj = Place(**new_place)
    setattr(city_obj, 'city_id', city_id)
    storage.new(city_obj)
    storage.save()
    return jsonify(city_obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """updates and to return the upadatedPlace with the status code 200"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")

    for key, value in req.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search/',
                 methods=['POST'], strict_slashes=False)
def place_search():
    '''retrieve specific places based on input'''
    content = request.get_json()
    if content is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    places_list = []
    if not content or not len(content):
        places_list = [di for di in storage.all(Place).values()]

    if "states" in content:
        for st_id in content['states']:
            di = storage.get(State, st_id)
            if di:
                for city in di.cities:
                    for place in city.places:
                        places_list.append(place)

    if "cities" in content:
        for city_id in content['cities']:
            di = storage.get(City, city_id)
            if di:
                for place in di.places:
                    if place not in places_list:
                        places_list.append(place)

    if "amenities" in content:
        if not places_list:
            places_list = [di for di in storage.all(Place).values()]
        amenities_list = [storage.get(Amenity, amenity_id) for
                          amenity_id in content['amenities']]
        places_list = [place for place in places_list if
                       all([am in place.amenities for am in amenities_list])]

    final_list = []
    for place in places_list:
        di = place.to_dict()
        di.pop('amenities', None)
        final_list.append(di)
    return jsonify(final_list)
