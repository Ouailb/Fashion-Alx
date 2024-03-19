#!/usr/bin/python3
from models import storage
from api.views.__init__ import app_views
from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token
from datetime import timedelta, datetime
from hashlib import md5

# def create_access_token(identity, expires_delta):
#     return identity + expires_delta

@app_views.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a Json"}), 400

    email = data.get('email', None)
    password = data.get('password', None)

    if not email or not password:
        return make_response(jsonify({"error": "Email and password are required"}), 400)

    user = storage.get_user_by_email(email=email)
    password = md5(password.encode()).hexdigest()

    if not user or user.password != password:
        return make_response(jsonify({"error": "Invalid email or password"}), 401)

    access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=365))
    response_data = {}
    response_data["token"] = access_token
    response_data["user_id"] = user.id
    response_data["message"] = "login successful"

    
    return make_response(jsonify(response_data), 200)
