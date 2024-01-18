#!/usr/bin/env python3
"""Session authentication module
"""
import os
from api.v1.views import app_views
from flask import request, jsonify, make_response
from models.user import User


@app_views.route('/auth_session/login',
                 methods=['POST'],
                 strict_slashes=False)
def login():
    """Login a user via session authentication
    """
    form = request.form
    email = form.get('email')
    if email is None or len(email) == 0:
        return jsonify({'error': 'email missing'}), 400
    password = form.get('password')
    if password is None or len(password) == 0:
        return jsonify({'error': 'password missing'}), 400
    users = User.search({'email': email})
    if len(users) == 0:
        return jsonify({'error': 'no user found for this email'}), 404
    user = None
    for user_obj in users:
        if user_obj.is_valid_password(password):
            user = user_obj
    if user is None:
        return jsonify({'error': 'wrong password'}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = make_response(user.to_json())
    response.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """Logout by deleting session
    """
    from api.v1.app import auth
    logout = auth.destroy_session(request)
    if logout:
        return jsonify({}), 200
    abort(404)
