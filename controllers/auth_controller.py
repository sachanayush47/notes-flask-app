from models.User import User
from config.db import db
from config.crypt import bcrypt
from utils.auth_utils import create_jwt, get_user_data


def login(username: str, password: str):
    try:
        if not username or not password:
            return {'message': 'Username and password are required'}, 400

        username = str(username)
        password = str(password)

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            jwt_token = create_jwt({'id': user.id})

            user_data = get_user_data(user)

            return {'message': f'Welcome {user.name}', 'token': jwt_token, 'user': user_data}, 200
        else:
            return {'message': 'Invalid username or password'}, 401
    except Exception as e:
        return {'message': str(e)}, 500


def signup(name: str, username: str, password: str):
    try:
        if not name or not username or not password:
            return {'message': 'Name, username and password are required'}, 400

        name = str(name)
        username = str(username)
        password = str(password)

        old_user = User.query.filter_by(username=username).first()
        if old_user:
            return {'message': 'Username already exists'}, 400

        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')
        new_user = User(name=name, username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return {'message': f'User created with {username}'}, 201
    except Exception as e:
        return {'message': str(e)}, 500
