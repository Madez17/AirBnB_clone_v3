#!/usr/bin/python3
"""comment of class"""

from api.v1.views import app_views
from models.state import State
from models import storage
from flask import Flask, jsonify, request, abort, make_response


@app_views.route("/states", strict_slashes=False, methods=['GET'])
def list_states_json():
    list_to_json = []
    all_objects = storage.all("State")

    for key, value in all_objects.items():
        list_to_json.append(value.to_dict())
    return (jsonify(list_to_json))


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def list_states_id(state_id):
    """Method list"""
    var = storage.get("State", state_id)
    if var is None:
        abort(404)
    else:
        objet_list = var.to_dict()
        return(jsonify(objet_list))


@app_views.route("/states/<state_id>",
                 methods=['DELETE'], strict_slashes=False)
def list_states_delete(state_id):
    """Method delete"""
    var = storage.get("State", state_id)
    if var is None:
        abort(404)
    else:
        storage.delete(var)
        storage.save()
        dict_state = {}
        return (jsonify(dict_state))


@app_views.route("/states", strict_slashes=False, methods=['POST'])
def post_states():
    """Method post"""
    if request.get_json():
        dic = request.get_json()
        if "name" in dic:
            name = State(**dic)
            name.save()
            return jsonify(name.to_dict()), 201
        else:
            return make_response(jsonify({'Missing name': 400}))
    else:
        return make_response(jsonify({'Not a JSON': 400}))


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
        return make_response(jsonify({'Not a JSON': 400}))
