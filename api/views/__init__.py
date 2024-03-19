#!/usr/bin/python3
""" Blueprint for API """
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api')

from api.views.status_view import *
from api.views.user_view import *
from api.views.product_view import *
from api.views.user_order_view import *
from api.views.order_items_view import *
from api.views.category_view import *
from api.views.login_view import *
from api.views.cart_view import *
