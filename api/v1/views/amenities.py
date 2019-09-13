#!/usr/bin/python3
"""comment of class"""

from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import Flask, jsonify, request, abort, make_response


@app_views.route("/amenities", strict_slashes=False, methods=['GET'])
def list_amenities_json():
    """Method GET"""
    amenities = storage.all("Amenity")
    amenities_list = []
    for key, value in amenities.items():
        amenities_list.append(value.to_dict())
    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def list_amenities_id(amenity_id):
    """Method list"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    format_amenity = amenity.to_dict()
    return jsonify(format_amenity)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def list_amenities_delete(amenity_id):
    """Method delete"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """Comment method"""
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    else:
        amenity_dict = request.get_json()
        if "name" in amenity_dict:
            amenity_name = amenity_dict["name"]
            amenity = Amenity(name=amenity_name)
            for k, v in amenity_dict.items():
                setattr(amenity, k, v)
            amenity.save()
            return jsonify(amenity.to_dict()), 201
        else:
            return jsonify({"error": "Missing name"}), 400


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Comment method"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400

    req = request.get_json()
    for k, v in req.items():
        if k != "id" or k != "created_at" or k != "updated_at":
            setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
