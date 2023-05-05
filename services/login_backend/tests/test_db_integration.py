
from app import create_app
import unittest

import os
import psycopg2

appurl = os.getenv('APPURL')
header = { "content-type": "application/json" }

class BackendDBIntegrationCase(unittest.TestCase):

    test_user1 = {
            'name': 'testuser1',
            'email': 'testuser1@gmail.com',
            'password': 'abc@123'
            }

    def create_app(self):
        self.dburi = "text_db"
        j.app.config['DATABASE'] = self.dburi
        j.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TESTDBURI')
        self.app = j.app.test_client()

    def setUp(self):
        self.create_app()
        try:
            conn = psycopg2.connect(
                database=self.dburi, user="root", password="root", host="localhost", port="5432")
        except Exception as e:
            print(e)
            exit(0) 

        cur = conn.cursor()
        try:
            cur.execute(
            "CREATE TABLE IF NOT EXISTS Users (id serial PRIMARY KEY, name varchar, email varchar, password varchar);")
        except Exception as e:
            print(e)
            exit(0) 
  
    def signup(self, name, password, email):
        url = "/signup"
        return self.app.post('/signup', data=dict(
            name=name,
            password=password,
            email=email,
        ), follow_redirects=True)

    def login(self, email, password):
        url = "/login"
        return self.app.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    # TEST CLASSES

    def test_register_login_logout_success(self):
        rv = self.signup(**self.test_user1)
        assert "Welcome %s!" % self.test_user1['name']  in rv.data
        rv = self.login(self.test_user1['email'],
                self.test_user1['password'])
        assert "Welcome %s!" % self.test_user1['email']  in rv.data
        rv = self.logout()
        assert "Logged out" in rv.data

if __name__ == "__main__":
    unittest.main()