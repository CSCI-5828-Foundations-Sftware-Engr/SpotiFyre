import unittest
from auth import auth
from flask import json
from app import create_app
from app.models import User, db as _db

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        _db.create_all()

    def tearDown(self):
        _db.session.remove()
        _db.drop_all()
        self.app_context.pop()

    def test_home_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_root_route(self):
        response = self.client.get('/test')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Welcome to login service!')

    def test_login_route(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_signup_route(self):
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)

    def test_signup_post(self):
        response = self.client.post('/signup', data=dict(email='test@test.com', name='Test User', password='test1234'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])

    def test_signup_existing_user(self):
        user = User(email='test@test.com', name='Test User', password='test1234')
        _db.session.add(user)
        _db.session.commit()

        response = self.client.post('/signup', data=dict(email='test@test.com', name='Test User', password='test1234'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_login_post_success(self):
        user = User(email='test@test.com', name='Test User', password='test1234')
        _db.session.add(user)
        _db.session.commit()

        response = self.client.post('/login', data=dict(email='test@test.com', password='test1234'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])

    def test_login_post_failure(self):
        response = self.client.post('/login', data=dict(email='test@test.com', password='wrongpassword'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_logout(self):
        user = User(email='test@test.com', name='Test User', password='test1234')
        _db.session.add(user)
        _db.session.commit()

        response = self.client.post('/login', data=dict(email='test@test.com', password='test1234'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])

        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])

# if __name__ == '__main__':
#     unittest.main()

