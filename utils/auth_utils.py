from datetime import datetime, timedelta
from dotenv import load_dotenv
import jwt
import os

load_dotenv()

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')


def decode_jwt(token):
    """Decodes a JWT token."""
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])


def create_jwt(data):
    """Creates a JWT token."""
    payload = {
        'data': data,
        'exp': datetime.utcnow() + timedelta(days=30),
        'iat': datetime.utcnow()
    }

    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
    return token


def get_user_data(user):
    user_data = user.__dict__
    user_data.pop('_sa_instance_state')
    user_data.pop('password')
    return user_data
