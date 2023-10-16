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
        self.assertEqual(resp_create.get_data(), b'"Campos obligatorios sin diligenciar"\n')
        self.assertEqual(resp_create.status_code, 400)

    def test_create_company_201_creation_success(self):
        new_company = {
            "tipoIde": "CC",
            "numeroIde": "123456",
            "razonsocial": "CompanyCO",
            "sector": "Financiero",
            "correo": "mail@companyco.co",
            "telefono": "1234567890",
            "direccion": "Av 123",
            "pais": "Colombia",
            "ciudad": "Bogota",
            "representante": self.data_factory.name(),
            "tpidrepresentante": "Cedula",
            "numidrepresentante": "123456"
        }
        resp_create = self.client.post(self.endpoint_create, headers={'Content-Type': 'application/json'}, data=json.dumps(new_company))
        print(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 201)

    def test_create_company_400_invalid_request(self):
        new_company = {
            "tipoIde": "CC",
            "numeroIde": "123456",
            "razonsocial": "CompanyCO",
            "sector": "Financiero",
            "correo": "mail@companyco.co",
            "telefono": "1234567890",
            "direccion": "Av 123",
            "pais": "Colombia",
            "ciudad": "Bogota",
            "representante": self.data_factory.name(),
            "tpidrepresentante": "CC",
            "numidrepresentante": "123456"
        }
        resp_create = self.client.post(self.endpoint_create, headers={'Content-Type': 'application/json'}, data=json.dumps(new_company))
        self.assertEqual(resp_create.get_data(), b'"Campos no cumplen requisitos minimos"\n')
        self.assertEqual(resp_create.status_code, 400)


    def test_get_all_companies_200(self):
        resp_get = self.client.get(self.endpoint_create, headers={'Content-Type': 'application/json'})
        print(resp_get.get_data())
        self.assertEqual(resp_get.status_code, 200)
