import json
from unittest import TestCase
from unittest.mock import MagicMock, patch
from app import app
from faker import Faker


class TestRecodScore(TestCase):
    """Class for test service"""

    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()
        self.idcandidatetest = self.data_factory.random_int(1, 20)
        self.endpoint_health = '/recordscore/ping'
        self.endpoint_get = '/recordscore/{}'.format(str(self.idcandidatetest)) 

    def test_health(self):
        """Test for health check ping"""
        req_health = self.client.get(self.endpoint_health, headers={'Content-Type': 'application/json'})
        json.loads(req_health.get_data())
        self.assertEqual(req_health.status_code, 200)

    def test_get_one_test_candidates(self):
        resp_get = self.client.get(self.endpoint_get, headers={'Content-Type': 'application/json'})
        self.assertEqual(resp_get.status_code, 200) 

    def test_put_recodscrore_400_request_empty(self):
        """Test for empty candidate"""
        new_recordscore = {}
        resp_put = self.client.put(self.endpoint_get, headers={'Content-Type': 'application/json'}, data=json.dumps(new_recordscore))
        error_code = json.loads(resp_put.get_data()).get('errorCode')
        self.assertEqual(error_code, 'CO01')
        self.assertEqual(resp_put.status_code, 400)

    #@patch('vistas.requests.post')
    #def test_create_candidate_201_creation_success(self, mock_post):
    def test_put_recordscore_200_creation_success(self):
        """Test for update candidateTest """
        new_recordscore = {
            "record": self.data_factory.random_int(1, 500)
        }
        resp_put = self.client.put(self.endpoint_get, headers={'Content-Type': 'application/json'}, data=json.dumps(new_recordscore))
        print(resp_put.get_data())
        self.assertEqual(resp_put.status_code, 200)