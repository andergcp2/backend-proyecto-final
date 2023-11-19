import json
from unittest import TestCase
from unittest.mock import MagicMock, patch
from app import app
from faker import Faker


class TestCandidateInterview(TestCase):
    """Class for test service"""

    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()
        self.endpoint_create = '/candidateInterview'
        self.endpoint_health = '/candidateInterview/ping'
        self.new_candidateinterview = {
                "candidateId" : self.data_factory.random_int(100, 500),
                "companyId" : self.data_factory.random_int(10, 20),
                "projectId" : self.data_factory.random_int(20, 80),
                "interviewDate" : "2023-12-19"
            }

    def test_health(self):
        """Test for health check ping"""
        req_health = self.client.get(self.endpoint_health, headers={'Content-Type': 'application/json'})
        json.loads(req_health.get_data())
        self.assertEqual(req_health.status_code, 200)
    
    def test_create_candidateinterview_400_request_empty(self):
        """Test for empty candidate"""
        new_candidateinterview = {}
        resp_create = self.client.post(self.endpoint_create, headers={'Content-Type': 'application/json'}, data=json.dumps(new_candidateinterview))
        error_code = json.loads(resp_create.get_data()).get('errorCode')
        self.assertEqual(error_code, 'CO01')
        self.assertEqual(resp_create.status_code, 400)
    
    #@patch('vistas.requests.post')
    #def test_create_candidate_201_creation_success(self, mock_post):
    def test_create_candidateinterview_201_creation_success(self):
        """Test for create candidate"""
        resp_create = self.client.post(self.endpoint_create, headers={'Content-Type': 'application/json'}, data=json.dumps(self.new_candidateinterview))
        print(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 201)
    
    def test_create_candidate_400_duplicate_request(self):
        new_candidateinterview = {
                "candidateId" : self.data_factory.random_int(50, 100),
                "companyId" : self.data_factory.random_int(1, 50),
                "projectId" : self.data_factory.random_int(1, 50),
                "interviewDate" : "2023-12-19"
            }
        resp_create = self.client.post(self.endpoint_create, headers={'Content-Type': 'application/json'}, data=json.dumps(new_candidateinterview))
        print(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 201)

        resp_create2 = self.client.post(self.endpoint_create, headers={'Content-Type': 'application/json'}, data=json.dumps(new_candidateinterview))
        error_code2 = json.loads(resp_create2.get_data()).get('errorCode')
        self.assertEqual(error_code2, 'CO05')
        self.assertEqual(resp_create2.status_code, 400)
    
    def test_create_candidate_400_invalid_request(self):
        new_candidateinterview = {
                "candidateId" : self.data_factory.random_int(50, 100),
                "companyId" : self.data_factory.random_int(1, 50),
                "projectId" : self.data_factory.random_int(1, 50),
                "interviewDate" : "2020"
            }
        resp_create = self.client.post(self.endpoint_create, headers={'Content-Type': 'application/json'}, data=json.dumps(new_candidateinterview))
        error_code = json.loads(resp_create.get_data()).get('errorCode')
        self.assertEqual(error_code, 'CO03')
        self.assertEqual(resp_create.status_code, 400)
    
    def test_create_candidate_400_date_invalid(self):
        new_candidateinterview = {
                "candidateId" : self.data_factory.random_int(50, 100),
                "companyId" : self.data_factory.random_int(1, 50),
                "projectId" : self.data_factory.random_int(1, 50),
                "interviewDate" : "2020-12-19"
            }
        resp_create = self.client.post(self.endpoint_create, headers={'Content-Type': 'application/json'}, data=json.dumps(new_candidateinterview))
        error_code = json.loads(resp_create.get_data()).get('errorCode')
        self.assertEqual(error_code, 'CO06')
        self.assertEqual(resp_create.status_code, 400)
     
    def test_get_all_candidatesinterview_200(self):
        resp_get = self.client.get(self.endpoint_create, headers={'Content-Type': 'application/json'})
        print(resp_get.get_data())
        self.assertEqual(resp_get.status_code, 200)

    def test_get_one_test_candidates(self):
        candidateId = self.data_factory.random_int(50, 100)
        new_candidateinterview = {
                "candidateId" : candidateId,
                "companyId" : self.data_factory.random_int(1, 50),
                "projectId" : self.data_factory.random_int(1, 50),
                "interviewDate" : "2020-12-19"
            }
        resp_create = self.client.post(self.endpoint_create, headers={'Content-Type': 'application/json'}, data=json.dumps(new_candidateinterview))
        print(resp_create.get_data())
        endpoint_get = '/candidateInterview/{}'.format(str(candidateId)) 
        resp_get = self.client.get(endpoint_get, headers={'Content-Type': 'application/json'})
        self.assertEqual(resp_get.status_code, 200)  
