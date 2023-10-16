import json
from app import app
from faker import Faker
from unittest import TestCase
from unittest.mock import patch
from datetime import datetime, timedelta

class TestCompany(TestCase):

    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()
        self.endpoint_create = '/companies'
        self.endpoint_health = '/companies/ping'
        
        '''self.token = "t0k3n"
        self.headers_token = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        
        self.id = self.data_factory.random_number(digits=3, fix_len=True)
        self.username = self.data_factory.word()
        self.email = self.data_factory.email()
        self.token_validation_resp = {'msg': {"id": self.id, "username": self.username, "email": self.email}, 'status_code': 200}'''

    def test_health(self):
        req_health = self.client.get(self.endpoint_health, headers={'Content-Type': 'application/json'})
        json.loads(req_health.get_data())
        self.assertEqual(req_health.status_code, 200)

