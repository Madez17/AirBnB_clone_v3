#!/usr/bin/python3
"""comment of class"""

from api.v1.views import app_views
import models
from flask import Flask, jsonify, request, abort


@app_views.route("/states", strict_slashes=False, methods=['GET'])
def list_states_json():
    list_to_json = []
    all_objects = models.storage.all("State")

    for key, value in all_objects.items():
        list_to_json.append(value.to_dict())
    return (jsonify(list_to_json))


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def list_states_id(state_id):
    var = models.storage.get("State", state_id)
    if var is None:
        abort(404)
    else:
        objet_list = var.to_dict()
        return(jsonify(objet_list))


@app_views.route("/states/<state_id>", methods=['DELETE'], strict_slashes=False)
def list_states_delete(state_id):
    var = models.storage.get("State", state_id)
    if var is None:
        abort(404)
    else:
        models.storage.delete(var)
        models.storage.save()
        dict_state = {}
        return (jsonify(dict_state))

@app_views.route("/states", strict_slashes=False, methods=['POST'])
    def fucn():
    try:
        if not request.is_json()
            raise JSONBadRequest('Not a JSON', 400)
        return "Not a JSON"
