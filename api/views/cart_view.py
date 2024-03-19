#!/usr/bin/python3
""" User view """
from models import storage
from models.cart import Cart
from models.user import User
from models.product import Product
from api.views.__init__ import app_views
from flask import jsonify, abort, make_response, request


@app_views.route('/users/<int:user_id>/cart', methods=['GET'], strict_slashes=False)
def get_user_cart(user_id):
    """
    Retrieves the list of all user objects
    or a specific user
    """
    user = storage.get_by_id(User, user_id)
    if not user:
        abort(404)
    cart = storage.get_by_id(Cart, user.cart_id)
    if not cart:
        abort(404)
    products_in_cart = [p.to_dict() for p in cart.products]
    return make_response(jsonify(products_in_cart), 200)

@app_views.route('/users/<int:user_id>/cart', methods=['POST'], strict_slashes=False)
def add_to_cart(user_id):
    """
    Retrieves the list of all user objects
    or a specific user
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a Json"}), 400
    user = storage.get_by_id(User, user_id)
    if not user:
        abort(404)
    cart = storage.get_by_id(Cart, user.cart_id)
    if not cart:
        abort(404)
    if not "product_id" in data:
        return make_response(jsonify({"description":"Missing product_id"}), 400)
    p_id = data.get("product_id")
    product = storage.get_by_id(Product, p_id)
    if not product:
        abort(404)
    if product not in cart.products:
        cart.products.append(product)
        cart.save()
        return make_response(jsonify({"description": "Product added to cart successfully", "total": len(cart.products)}), 201)
    else:
        return make_response(jsonify({"description": "Product already in cart"}), 400)

@app_views.route('/users/<int:user_id>/cart/<int:product_id>', methods=['DELETE'], strict_slashes=False)
def remove_from_cart(user_id, product_id):
    """
    Retrieves the list of all user objects
    or a specific user
    """
    user = storage.get_by_id(User, user_id)
    if not user:
        abort(404)
    cart = storage.get_by_id(Cart, user.cart_id)
    if not cart:
        abort(404)
    product = storage.get_by_id(Product, product_id)
    if not product or product not in cart.products:
        abort(404)
    cart.products.remove(product)
    cart.save()
    return make_response(jsonify({"description": "Product removed from cart successfully", "left": len(cart.products)}), 201)
