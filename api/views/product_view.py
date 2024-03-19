#!/usr/bin/python3
""" User view """
from models import storage
from models.product import Product
from api.views.__init__ import app_views
from flask import jsonify, abort, make_response, request



@app_views.route('/products', methods=['GET'], strict_slashes=False)
def get_products():
    """
    Retrieves the list of all user objects
    or a specific user
    """
    category_name = request.args.get('category_name')
    category_type = request.args.get('category_type')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    limit = request.args.get('limit')
    order_asc = request.args.get('order_asc')
    order_desc = request.args.get('order_desc')
    start_from = request.args.get('from')
    ignore = request.args.get('ignore')
    filter = {}
    if category_type:
        filter['category_type'] = category_type

    filtered_products = [pd.to_dict() for pd in storage.all(Product, order_asc=order_asc, order_desc=order_desc, filter=filter).values()]


    # Filter products by category if 'category_name' parameter is provided
    if category_name:
        filtered_products = [p for p in filtered_products if p['category_name'] == category_name]

    # Filter products by minimum price if 'min_price' parameter is provided
    if min_price:
        min_price = float(min_price)
        filtered_products = [p for p in filtered_products if p['price'] >= min_price]

    # Filter products by maximum price if 'max_price' parameter is provided
    if max_price:
        max_price = float(max_price)
        filtered_products = [p for p in filtered_products if p['price'] <= max_price]

    if start_from and start_from.isdigit():
        start_from = int(start_from)
        filtered_products = filtered_products[start_from:]

    if ignore and ignore.isdigit():
        ignore = int(ignore)
        filtered_products = [p for p in filtered_products if p['id'] != ignore]
    
    # Limit the number of products if 'limit' parameter is provided
    if limit and limit.isdigit():
        limit = int(limit)
        filtered_products = filtered_products[:limit]

    return make_response(jsonify(filtered_products), 200)

@app_views.route('/products/<int:id>', methods=['GET'], strict_slashes=False)
def get_product_by_id(id=None):
    """get product by id """
    product = storage.get_by_id(Product, id)
    if not product:
        abort(404)
    return make_response(jsonify(product.to_dict()), 200)


@app_views.route('/products/<int:id>', methods=['DELETE'], strict_slashes=False)
def delete_product(id):
    """
    Deletes a user Object
    """
    product = storage.get_by_id(Product, id)
    if not product:
        abort(404)

    product.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/products', methods=['POST'], strict_slashes=False)
def post_product():
    """
    Creates a user
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'title' not in data:
        abort(400, description="Missing title")
    if 'price' not in data:
        abort(400, description="Missing price")
    if 'description' not in data:
        abort(400, description="Missing description")
    if 'category_name' not in data:
        abort(400, description="Missing category_name")
    if 'category_type' not in data:
        abort(400, description="Missing category_type")


    instance = Product(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/products/<int:id>', methods=['PUT'], strict_slashes=False)
def put_product(id):
    """
    Updates a product
    """
    product = storage.get_by_id(Product, id)

    if not product:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at', 'product_code']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore and hasattr(product, key):
            setattr(product, key, value)
    storage.save()
    return make_response(jsonify(product.to_dict()), 200)
