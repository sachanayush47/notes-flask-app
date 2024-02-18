from flask import Blueprint, request, jsonify, make_response
from controllers.auth_controller import login, signup

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login_route():
    request_data = request.get_json()
    username = request_data.get('username')
    password = request_data.get('password')

    login_response, status_code = login(username, password)

    if 'token' in login_response:
        token = login_response['token']
        login_response.pop('token')
        response = make_response(jsonify(login_response), status_code)
        response.set_cookie('token', token, httponly=True)
        return response
    else:
        return jsonify(login_response), status_code


@auth_bp.route('/signup', methods=['POST'])
def signup_route():
    request_data = request.get_json()
    name = request_data.get('name')
    username = request_data.get('username')
    password = request_data.get('password')

    signup_response, status_code = signup(name, username, password)

    return jsonify(signup_response), status_code
