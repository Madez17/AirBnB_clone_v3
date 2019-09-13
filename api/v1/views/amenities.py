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


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def list_amenities_id(amenity_id):
    """Method list"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    else:
        format_amenity = amenity.to_dict()
        return jsonify(format_amenity)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def list_amenities_delete(amenity_id):
    """Method delete"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()
        return jsonify({})


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def post_amenities():
    """Method post"""
    if request.get_json():
        amenity_req = request.get_json()
        if "name" in dic:
            name = Amenity(**amenity_req)
            name.save()
            return jsonify(name.to_dict()), 201
        else:
            return make_response(jsonify({'error': 'Missing name'}), 400)
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_ameniy(amenity_id):
    """Method put"""
    amenity = storage.get("Amenity", amenity_id)
    restrictions = ["id", "update_at", "create_at"]
    if amenity is None:
        abort(404)
    elif request.get_json():
        req = request.get_json()
        for key, value in req.items():
            if key not in restrictions:
                setattr(var, key, value)
        amenity.save()
        return jsonify(amenity.to_dict())
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
