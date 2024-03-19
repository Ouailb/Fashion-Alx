#!/usr/bin/python3
""" User view """
from models import storage
from api.views.__init__ import app_views
from flask import jsonify,  request, make_response


@app_views.route('/products/Men/<ctgName>', methods=['GET'], strict_slashes=False)
@app_views.route('/products/Women/<ctgName>', methods=['GET'], strict_slashes=False)
def products_by_category(ctgName):
    """
    Retrieves the list of all user objects
    or a specific user
    """
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    limit = request.args.get('limit')
    order_asc = request.args.get('order_asc')
    order_desc = request.args.get('order_desc')
    start_from = request.args.get('from')
    ignore = request.args.get('ignore')
    route = request.url_rule.rule
    c_type = 'Women' if 'Women' in route else 'Men'
    filtered_products = [pd.to_dict() for pd in storage.filter_product(c_type=c_type, c_name=ctgName, order_asc=order_asc, order_desc=order_desc).values()]

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
