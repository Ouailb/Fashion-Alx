#!/usr/bin/python3
""" User view """
from models import storage
from models.order import Order
from models.user import User
from api.views.__init__ import app_views
from flask import jsonify, abort, make_response, request


@app_views.route('/users/<int:user_id>/orders', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<int:user_id>/orders/<int:order_id>', methods=['GET'], strict_slashes=False)
def get_user_orders(user_id, order_id=None):
    """
    Retrieves the list of all user objects
    or a specific user
    """
    user = storage.get_by_id(User, user_id)
    if not user:
        abort(404)
    if not order_id:
        return make_response(jsonify([order.to_dict() for order in user.orders]), 200)
    else:
        for order in user.orders:
            if order.id == order_id:
                return make_response(jsonify(order.to_dict()), 200)
        abort(404)



# @app_views.route('/users/<int:user_id>/orders/<int:order_id>', methods=['DELETE'], strict_slashes=False)
# def delete_order(user_id, order_id):
#     """
#     Deletes a user Object
#     """
#     user = storage.get_by_id(User, user_id)
#     if not user:
#         abort(404)

#     else:
#         for order in user.orders:
#             if order.id == order_id:
#                 order.delete()
#                 storage.save()
#                 return make_response(jsonify({}), 200)
#         abort(400,  description="Order does not exists")


@app_views.route('/users/<int:user_id>/orders', methods=['POST'], strict_slashes=False)
def post_order(user_id):
    """
    Creates a user
    """
    user = storage.get_by_id(User, user_id)
    if not user:
        abort(404)

    instance = Order(user_id=user_id)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/users/<int:user_id>/orders/<int:order_id>', methods=['PUT'], strict_slashes=False)
def put_order(user_id, order_id):
    """
    Updates a product
    """
    user = storage.get_by_id(User, user_id)
    if not user:
        abort(404)

    for order in user.orders:
        if order.id == order_id:
            if not request.get_json():
                abort(400, description="Not a JSON")
            ignore = ['id', 'created_at', 'updated_at', 'user_id']
            data = request.get_json()
            for key, value in data.items():
                if key not in ignore and hasattr(order, key):
                    setattr(order, key, value)
            storage.save()
            return make_response(jsonify(order.to_dict()), 200)
    abort(404)
