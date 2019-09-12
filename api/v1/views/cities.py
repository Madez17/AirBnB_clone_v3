#!/usr/bin/python3
"""comment of class"""
from api.v1.views import app_views
from models.state import State, City
from models import storage
from flask import Flask, jsonify, request, abort, make_response
@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=['GET'])
def list_cities_json(state_id):
    """ Method GET show all Cities"""
    list_city_to_json = []
    filter_states = storage.get("State", state_id)
    if filter_states is None:
        abort(404)
    else:
        for iter in filter_states.cities:
            list_city_to_json.append(iter.to_dict())
