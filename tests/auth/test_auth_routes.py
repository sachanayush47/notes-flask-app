import unittest
import json
from flask import current_app
from app import create_app, db
from models.User import User
from config.crypt import bcrypt


class AuthRoutesTestCase(unittest.TestCase):
    BASE_URL = '/api/v1/auth'

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_signup_new_user(self):
        response = self.client.post(f'{self.BASE_URL}/signup', json={
            'name': 'John Doe',
            'username': 'johndoe',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('User created with johndoe', response.json['message'])

    def test_login_valid_user(self):
        hashed_password = bcrypt.generate_password_hash(
            'testpassword').decode('utf-8')
        user = User(name='Test User', username='testuser',
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()

        response = self.client.post(f'{self.BASE_URL}/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        # Check for the 'token' cookie in the response headers
        cookies = response.headers.getlist('Set-Cookie')
        token_cookie = [cookie for cookie in cookies if 'token=' in cookie]
        self.assertTrue(len(token_cookie) > 0,
                        "Token cookie not set in response")
        self.assertIn('Welcome Test User', response.json['message'])

    def test_login_with_invalid_username(self):
        response = self.client.post(f'{self.BASE_URL}/login', data=json.dumps({
            'username': 'nonexistent',
            'password': 'test'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid username or password', response.json['message'])

    def test_login_with_invalid_password(self):
        response = self.client.post(f'{self.BASE_URL}/login', data=json.dumps({
            'username': 'testuser',
            'password': 'incorrectpassword'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid username or password', response.json['message'])

    def test_signup_with_duplicate_username(self):
        new_user = User(name='Another Test User',
                        username='johndoe', password='somepassword')
        db.session.add(new_user)
        db.session.commit()

        response = self.client.post(f'{self.BASE_URL}/signup', data=json.dumps({
            'name': 'Another Test User',
            'username': 'johndoe',  # Duplicate username
            'password': 'somepassword'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Username already exists', response.json['message'])


if __name__ == '__main__':
    unittest.main()
