import json
from unittest import TestCase
from app import app
from faker import Faker


class TestCompany(TestCase):
    """Class for test service"""

    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()
        self.endpoint_get = '/candidates-qry'
        self.endpoint_health = '/candidates-qry/ping'

    def test_health(self):
        """Test for health check ping"""
        req_health = self.client.get(self.endpoint_health, headers={'Content-Type': 'application/json'})
        json.loads(req_health.get_data())
        self.assertEqual(req_health.status_code, 200)

    def test_get_all_companies_200(self):
        """Test get all candidates"""
        resp_get = self.client.get(self.endpoint_get, headers={'Content-Type': 'application/json'})
        print(resp_get.get_data())
        self.assertEqual(resp_get.status_code, 200)

    def test_get_companies_404(self):
        """Test get all candidates"""
        resp_get = self.client.get(self.endpoint_get+"?role=Any", headers={'Content-Type': 'application/json'})
        print(resp_get.get_data())
        self.assertEqual(resp_get.status_code, 404)
