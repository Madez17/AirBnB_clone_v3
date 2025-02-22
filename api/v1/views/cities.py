#!/usr/bin/python3
"""comment of class"""
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage
from flask import Flask, jsonify, request, abort, make_response


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=['GET'])
def list_cities_json(state_id):
    """ Method GET show all Cities """
    list_city_to_json = []
    filter_states = storage.get("State", state_id)
    if filter_states is None:
        abort(404)
    else:
        for itera in filter_states.cities:
            list_city_to_json.append(itera.to_dict())
        return jsonify(list_city_to_json)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def list_cities_id(city_id):
    """ doc """
    filter_id_city = storage.get("City", city_id)
    if filter_id_city is None:
        abort(404)
    return jsonify(filter_id_city.to_dict())


@app_views.route("/cities/<city_id>",
                 methods=['DELETE'], strict_slashes=False)
def list_cities_delete(city_id):
    """ Method delete """
    filter_id_city = storage.get("City", city_id)
    if filter_id_city is None:
        abort(404)
    else:
        storage.delete(filter_id_city)
        storage.save()
        dict_state = {}
        return (jsonify(dict_state))


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=['POST'])
def post_city(state_id):
    """ Method post """
    filter_state = storage.get("State", state_id)
    if filter_state is None:
        abort(404)
    if request.is_json:
        dic = request.get_json()
        if "name" in dic:
            dic["state_id"] = state_id
            name = City(**dic)
            name.save()
            return jsonify(name.to_dict()), 201
        else:
            return make_response(jsonify({'error': 'Missing name'}), 400)
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['PUT'])
def put_cities(city_id):
    """ Method put """
    filter_id_city = storage.get("City", city_id)
    restrictions = ["id", "update_at", "create_at", "state_id"]
    if filter_id_city is None:
        abort(404)
    if request.is_json:
        req = request.get_json()
        for key, value in req.items():
            if key not in restrictions:
                setattr(filter_id_city, key, value)
        filter_id_city.save()
        return jsonify(filter_id_city.to_dict())
    else:
        return make_response(jsonfilter_id_city({'error': 'Not a JSON'}), 400)
