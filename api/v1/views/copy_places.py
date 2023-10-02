#!/usr/bin/python3
'''places APIs'''
from api.v1.views import app_views
from flask import abort, request, jsonify, make_response
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from model.amenity import Amenity

@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places(city_id):
    ''' get all places in city'''
    di = storage.get(City, city_id)
    if not di:
        abort(404)
    cities_list = []
    for place in di.places:
        di = place.to_dict()
        cities_list.append(di)
    return jsonify(cities_list)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    '''get all cities or a specific city by id'''
    di = storage.get(Place, place_id)
    if di:
        return jsonify(di.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    '''DELETE method'''
    di = storage.get(Place, place_id)
    if not di:
        abort(404)
    storage.delete(di)
    storage.save()
    return jsonify({})


@app_views.route('cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    '''POST method'''
    di = storage.get(City, city_id)
    if not di:
        abort(404)
    content = request.get_json()
    if not content:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in content:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if not storage.get(User, content['user_id']):
        abort(404)
    if "name" not in content:
        return make_response(jsonify({"error": "Missing name"}), 400)
    content['city_id'] = city_id
    ct = Place(**content)
    storage.new(ct)
    storage.save()
    return (jsonify(ct.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    '''PUT method'''
    di = storage.get(Place, place_id)
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


@app_views.route('/places_search/',
                 methods=['POST'], strict_slashes=False)
def place_search():
    '''retrieve specific places based on input'''
    content = request.get_json()
    if not content:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    places_list = []
    if content == [] or (len(content) == 1 and 'amenities' in content):
        places_list = [di for di in storage.all(Place).values()]
    
    searched_cities = []
    
    if "states" in content:
            for st_id in content['states']:
                di = storage.get(State, st_id)
                for city in di.cities:
                    searched_cities.append(city.id)
                    for place in city.places:
                        places_list.append(place)

    if "cities" in content:
        for city_id in content['cities']:
            if city_id not in searched_cities:
                searched_cities.append(city_id)
                di = storage.get(City, city_id)
                for place in city.places:
                        places_list.append(place)
    
    if "amenities" in content:
        amenities_list = [storage.get(Amenity, amenity_id) for
                          amenity_id in content['amenities']]
        # for amenity_id in content['amenities']:
        #    di = storage.get(Amenity, amenity_id)
        final_list = [place.to_dict() for place in places_list if 
                    all([am in place.amenities for am in amenities_list])]
            
    return jsonify(final_list)

