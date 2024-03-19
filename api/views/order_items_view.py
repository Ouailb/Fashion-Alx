#!/usr/bin/python3
""" User view """
from models import storage
from models.product import Product
from models.order_items import OrderItem
from models.user import User
from api.views.__init__ import app_views
from flask import jsonify, abort, make_response, request


@app_views.route('/users/<int:user_id>/orders/<int:order_id>/items', methods=['GET'], strict_slashes=False)
def get_item(user_id, order_id):
    """
    Retrieves the list of all user objects
    or a specific user
    """
    user = storage.get_by_id(User, user_id)
    if not user:
        abort(404)
    order = None
    for ord in user.orders:
        if ord.id == order_id:
            order = ord
            break
    if not order:
        abort(404)
    return make_response(jsonify([item.to_dict() for item in order.order_items]), 200)



@app_views.route('/users/<int:user_id>/orders/<int:order_id>/items/<int:item_id>', methods=['DELETE'], strict_slashes=False)
def delete_item(user_id, order_id, item_id):
    """
    Deletes a user Object
    """
    user = storage.get_by_id(User, user_id)
    if not user:
        abort(404)
    order = None
    for ord in user.orders:
        if ord.id == order_id:
            order = ord
            break
    if not order:
        abort(400,  description="Order does not exists")
    for item in order.order_items:
        if item.id == item_id:
            item.delete()
            storage.save()
            return make_response(jsonify({}), 200)
    abort(400,  description="item does not exists")


@app_views.route('/users/<int:user_id>/orders/<int:order_id>/items/', methods=['POST'], strict_slashes=False)
def post_item(user_id, order_id):
    """
    Creates a user
    """
    user = storage.get_by_id(User, user_id)
    if not user:
        abort(404)
    order = None
    for ord in user.orders:
        if ord.id == order_id:
            order = ord
            break
    if not order:
        abort(400,  description="Order does not exists")

    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    if 'product_id' not in data:
        abort(400, description="Missing product ID")
    product_id = data.get("product_id")
    product = storage.get_by_id(Product, product_id)
    if not product: 
        abort(400, description="Product Unavailable")
    quantity = data.get("item_quantity", 1)
    instance = OrderItem(order_id=order_id, product_id=product_id, item_quantity=quantity)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)
