#!/usr/bin/python3
"""comment of class"""

from api.v1.views import app_views
from models.user import User
from models import storage
from flask import Flask, jsonify, request, abort, make_response


@app_views.route("/users", strict_slashes=False, methods=['GET'])
def list_user_json():
    """ Method GET show all users"""
    list_to_json = []
    all_objects = storage.all("User")

    for key, value in all_objects.items():
        list_to_json.append(value.to_dict())
    return (jsonify(list_to_json))


@app_views.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def list_users_id(user_id):
    """Method list"""
    var = storage.get("User", user_id)
    if var is None:
        abort(404)
    else:
        objet_list = var.to_dict()
        return(jsonify(objet_list))


@app_views.route("/users/<user_id>",
                 methods=['DELETE'], strict_slashes=False)
def list_users_delete(user_id):
    """Method delete"""
    var = storage.get("User", user_id)
    if var is None:
        abort(404)
    else:
        storage.delete(var)
        storage.save()
        dict_state = {}
        return (jsonify(dict_state))


@app_views.route("/users", strict_slashes=False, methods=['POST'])
def post_users():
    """Method post"""
    if request.get_json():
        dic = request.get_json()
        for key, value in dic.items():
            if key != "email":
                return make_response(jsonify({"error": 'Missing email'}), 400)
            if key != "password":
                return make_response(jsonify({"error": 'Missing password'}),
                                              400)
        
        user = User(**dic)
        user.save()
        return jsonify(user.to_dict()), 201
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)


@app_views.route("/users/<user_id>", strict_slashes=False, methods=['PUT'])
def put_users(state_id):
    """Method put"""
    var = storage.get("User", user_id)
    restrictions = ["id", "email", "update_at", "create_at"]
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
