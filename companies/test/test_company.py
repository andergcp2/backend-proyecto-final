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

    def test_create_company_400_request_empty(self):
        new_company = {}
        resp_create = self.client.post(self.endpoint_create, headers={'Content-Type': 'application/json'}, data=json.dumps(new_company))
        error_code = json.loads(resp_create.get_data()).get('errorCode') 
        self.assertEqual(error_code, 'CO01')
        self.assertEqual(resp_create.status_code, 400)

    def test_create_company_201_creation_success(self):
        new_company = {
            "idType": "NIT",
            "idNumber": 123456,
            "companyName": "CompanyCO",
            "industry": "Financiero",
            "email": "mail@companyco.co",
            "phone": 1234567890,
            "address": "Av 123",
            "country": "Colombia",
            "city": "Bogota",
            "reprName": self.data_factory.name(),
            "reprIdType": "CC",
            "reprIdNumber": 123456
        }
        resp_create = self.client.post(self.endpoint_create, headers={'Content-Type': 'application/json'}, data=json.dumps(new_company))
        print(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 201)

    def test_create_company_400_invalid_request(self):
        new_company = {
            "idType": "C",
            "idNumber": "123456",
            "companyName": "CompanyCO",
            "industry": "Financiero",
            "email": "mail@companyco.co",
            "phone": "1234567890",
            "address": "Av 123",
            "country": "Colombia",
            "city": "Bo",
            "reprName": self.data_factory.name(),
            "reprIdType": "C",
            "reprIdNumber": "123456"
        }
        resp_create = self.client.post(self.endpoint_create, headers={'Content-Type': 'application/json'}, data=json.dumps(new_company))
        error_code = json.loads(resp_create.get_data()).get('errorCode') 
        self.assertEqual(error_code, 'CO02')
        self.assertEqual(resp_create.status_code, 400)


    def test_get_all_companies_200(self):
        resp_get = self.client.get(self.endpoint_create, headers={'Content-Type': 'application/json'})
        print(resp_get.get_data())
        self.assertEqual(resp_get.status_code, 200)
