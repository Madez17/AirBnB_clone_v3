#!/usr/bin/python3
"""comment of class"""

from api.v1.views import app_views
from models.state import State
from models import storage, Place, City, User
from flask import Flask, jsonify, request, abort, make_response


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def list_place(city_id):
    """ Retrieves the list of all Place objects of a City """
    var = []
    city_obj = storage.get('City', city_id)
    if city_obj is None:
        abort(404)
    for key, value in storage.all("Place").items():
        if value.city_id == city_id:
            var.append(value.to_dict())
    return jsonify(var)


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def list_places_id(place_id):
    """Method list"""
    var = storage.get("Place", place_id)
    if var is None:
        abort(404)
    else:
        objet_list = var.to_dict()
        return(jsonify(objet_list))


@app_views.route("/places/<place_id>",
                 methods=['DELETE'], strict_slashes=False)
def list_place_delete(place_id):
    """Method delete"""
    var = storage.get("Place", place_id)
    if var is None:
        abort(404)
    else:
        storage.delete(var)
        storage.save()
        return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=['POST'])
def post_place():
    """Method post"""
    dic = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    user_ = request.get_json()
    if "user_id" not in user_:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    get_user = storage.get("User", user_["user_id"])
    if get_user is None:
        abort(404)
    if "name" not in dic:
        return make_response(jsonify({"error": "Missing name"}), 400)
    place_ = Place(**user_)
    place_.save()
    return jsonify(place_.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False, methods=['PUT'])
def put_states(state_id):
    """Method put"""
    var = storage.get("State", state_id)
    restrictions = ["id", "update_at", "create_at"]
    if var is None:
        abort(404)
    if request.get_json():
        req = request.get_json()
        for key, value in req.items():
            if key not in restrictions:
                setattr(var, key, value)
        var.save()
        return jsonify(var.to_dict())
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
