#!/usr/bin/python3
"""comment of class"""

from api.v1.views import app_views
from models.user import User
from models.review import Review
from models.place import Place
from models import storage
from flask import Flask, jsonify, request, abort, make_response


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=['GET'])
def list_review_json():
    """ Method GET show all Places """
    list_to_json = []
    all_objects = storage.all("Place")

    for key, value in all_objects.items():
        list_to_json.append(value.to_dict())
    return (jsonify(list_to_json))


@app_views.route("/reviews/<review_id>", methods=['GET'],
                 strict_slashes=False)
def list_review_id(review_id):
    """Method list"""
    var = storage.get("Review", review_id)
    if var is None:
        abort(404)
    else:
        objet_list = var.to_dict()
        return(jsonify(objet_list))


@app_views.route("/reviews/<review_id>",
                 methods=['DELETE'], strict_slashes=False)
def list_review_delete(review_id):
    """Method delete"""
    var = storage.get("Review", review_id)
    if var is None:
        abort(404)
    else:
        storage.delete(var)
        storage.save()
        dict_state = {}
        return (jsonify(dict_state), 200)


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=['POST'])
def post_reviw(place_id):
    """Method post"""
    filter_place = storage.get("Place", place_id)
    if filter_place is None:
        abort(404)

    if request.get_json():
        dic = request.get_json()
        if "user" not in dic:
            return make_response(jsonify({"error": 'Missing user_id'}), 400)
        else:
            user = storage.get("User", dic["user"])
            if user is None:
                abort(404)
        if "text" not in dic:
            return make_response(jsonify
                                 ({"error": 'Missing text'}), 400)
        review = Review(**dic)
        review.save()
        return jsonify(user.to_dict()), 201
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=['PUT'])
def put_review(review_id):
    """Method put"""
    var = storage.get("Review", review_id)
    restrictions = ["id", "user_id", "place_id", "update_at", "create_at"]
    if var is None:
        abort(404)
    if request.get_json():
        req = request.get_json()
        for key, value in req.items():
            if key not in restrictions:
                setattr(var, key, value)
        var.save()
        return jsonify(var.to_dict()), 200
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
