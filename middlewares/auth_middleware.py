from flask import request, jsonify
from functools import wraps

from models.User import User
from utils.auth_utils import decode_jwt, get_user_data

def verify_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check if token is passed in the request headers
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Decode the token
            data = decode_jwt(token)
            user = User.query.get(data['data']['id'])
            user_data = get_user_data(user)
            if user:
                request.user = user_data
            else:
                return jsonify({'message': 'User not found!'}), 404
        except Exception as e:
            print(e)
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)

    return decorated
