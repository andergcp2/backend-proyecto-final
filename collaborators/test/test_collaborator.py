import json
from app import app
from faker import Faker
from unittest import TestCase
from unittest.mock import patch
from datetime import datetime, timedelta

class TestCollaborator(TestCase):

    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()
        self.endpoint_create = '/collaborators'
        self.endpoint_health = '/collaborators/ping'
        
    def test_health(self):
        req_health = self.client.get(self.endpoint_health, headers={'Content-Type': 'application/json'})
        json.loads(req_health.get_data())
        self.assertEqual(req_health.status_code, 200)

    def test_create_collaborator_400_request_empty(self):
        new_collaborator = {}
        resp_create = self.client.post(self.endpoint_create, headers={'Content-Type': 'application/json'}, data=json.dumps(new_collaborator))
        error_code = json.loads(resp_create.get_data()).get('errorCode') 
        self.assertEqual(error_code, 'CO01')
        self.assertEqual(resp_create.status_code, 400)

    def test_create_company_201_creation_success(self):
        new_company = {
            "idType" : "CC",
            "idNumber" : self.data_factory.random_int(10000, 32000),
            "collaboratorName" : self.data_factory.first_name(), 
            "collaboratorLastName" : self.data_factory.last_name(),
            "email" : self.data_factory.email(),
            "phone" : self.data_factory.random_int(20000, 50000),
            "address" : self.data_factory.address(),
            "role" : "Reclutador",
            "position" : self.data_factory.job()
        }
        resp_create = self.client.post(self.endpoint_create, headers={'Content-Type': 'application/json'}, data=json.dumps(new_company))
        print(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 201)

    def test_create_collaborator_400_invalid_request(self):
        new_company = {
            "idType" : "C",
            "idNumber" : self.data_factory.random_int(10000, 32000),
            "collaboratorName" : self.data_factory.first_name(), 
            "collaboratorLastName" : self.data_factory.last_name(),
            "email" : self.data_factory.email(),
            "phone" : self.data_factory.random_int(20000, 50000),
            "address" : self.data_factory.address(),
            "role" : "Rec",
            "position" : self.data_factory.job()
        }
        resp_create = self.client.post(self.endpoint_create, headers={'Content-Type': 'application/json'}, data=json.dumps(new_company))
        error_code = json.loads(resp_create.get_data()).get('errorCode') 
        self.assertEqual(error_code, 'CO02')
        self.assertEqual(resp_create.status_code, 400)


    def test_get_all_collaborators_200(self):
        resp_get = self.client.get(self.endpoint_create, headers={'Content-Type': 'application/json'})
        print(resp_get.get_data())
        self.assertEqual(resp_get.status_code, 200)

    def test_create_collaborator_400_user_duplicate(self):
        idnum = self.data_factory.random_int(10000, 32000)
        new_collaborator = {
            "idType" : "CC",
            "idNumber" : idnum,
            "collaboratorName" : self.data_factory.first_name(), 
            "collaboratorLastName" : self.data_factory.last_name(),
            "email" : self.data_factory.email(),
            "phone" : self.data_factory.random_int(20000, 50000),
            "address" : self.data_factory.address(),
            "role" : "Recluctador",
            "position" : self.data_factory.job()
        }

        resp_create = self.client.post(self.endpoint_create, headers={'Content-Type': 'application/json'}, data=json.dumps(new_collaborator))
        print(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 201)

        new_collaborator2 = {
            "idType" : "CC",
            "idNumber" : idnum,
            "collaboratorName" : self.data_factory.first_name(), 
            "collaboratorLastName" : self.data_factory.last_name(),
            "email" : self.data_factory.email(),
            "phone" : self.data_factory.random_int(20000, 50000),
            "address" : self.data_factory.address(),
            "role" : "Recluctador",
            "position" : self.data_factory.job()
        }
        resp_create = self.client.post(self.endpoint_create, headers={'Content-Type': 'application/json'}, data=json.dumps(new_collaborator2))
        error_code = json.loads(resp_create.get_data()).get('errorCode') 
        self.assertEqual(error_code, 'CO03')
        self.assertEqual(resp_create.status_code, 400)
