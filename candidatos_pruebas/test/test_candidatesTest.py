import json
from unittest import TestCase
from unittest.mock import MagicMock, patch
from app import app
from faker import Faker
import datetime as dt
from datetime import timedelta
from modelos import db, CandidateTest


class TestCandidateTest(TestCase):
    """Class for test service"""

    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()

        cand_test1 = CandidateTest(
            idcandidate = self.data_factory.random_int(100, 999), 
            idtest = self.data_factory.random_int(10, 99),
            maxdatepresent = dt.date.today()+timedelta(days=15),
            testestatus = "ASIGNADA")
        
        cand_test2 = CandidateTest(
            idcandidate = self.data_factory.random_int(100, 999), 
            idtest = self.data_factory.random_int(10, 99),
            maxdatepresent = dt.date.today()+timedelta(days=15),
            testestatus = "FINALIZADA")

        db.session.add(cand_test1)
        db.session.add(cand_test2)
        db.session.commit()

        self.candidatoId     = cand_test1.idcandidate
        self.candidatoDoneId = cand_test2.idcandidate
        self.pruebaId        = cand_test1.idtest
        self.pruebaDoneId    = cand_test2.idtest

        self.endpoint_create = '/candidateTest'
        self.endpoint_health = '/candidateTest/ping'
        self.endpoint_get_404 = '/candidateTest/{}/{}'.format(str(self.candidatoId*1000), str(self.pruebaId*1000))
        self.endpoint_get_412 = '/candidateTest/{}/{}'.format(str(self.candidatoDoneId), str(self.pruebaDoneId))
        self.endpoint_get_200 = '/candidateTest/{}/{}'.format(str(self.candidatoId), str(self.pruebaId))

        self.headers = {'Content-Type': 'application/json'}
        self.data = {'record': round (self.data_factory.random_int(0, 5), 2)}

    def test_health(self):
        # """Test for health check ping"""
        req_health = self.client.get(self.endpoint_health, headers = self.headers)
        json.loads(req_health.get_data())
        self.assertEqual(req_health.status_code, 200)
    
    def test_create_candidatetest_400_request_empty(self):
        # """Test for empty candidate"""
        new_candidatetest = {}
        resp_create = self.client.post(self.endpoint_create, headers = self.headers, data=json.dumps(new_candidatetest))
        error_code = json.loads(resp_create.get_data()).get('errorCode')
        self.assertEqual(error_code, 'CO01')
        self.assertEqual(resp_create.status_code, 400)
    
    #@patch('vistas.requests.post')
    #def test_create_candidate_201_creation_success(self, mock_post):
    def test_create_candidate_201_creation_success(self):
        # """Test for create candidate"""
        new_candidatetest = {
            "idcandidate": self.data_factory.random_int(1, 500),
            "idtest": self.data_factory.random_int(1, 100)
        }

        resp_create = self.client.post(self.endpoint_create, headers = self.headers, data=json.dumps(new_candidatetest))
        #print(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 201)
    
    def test_create_candidate_400_invalid_request(self):
        new_candidatetest = {
            "idcandidate": self.data_factory.name(),
            "idtest": self.data_factory.name()
        }
        resp_create = self.client.post(self.endpoint_create, headers = self.headers, data=json.dumps(new_candidatetest))
        error_code = json.loads(resp_create.get_data()).get('errorCode')
        self.assertEqual(error_code, 'CO03')
        self.assertEqual(resp_create.status_code, 400)

    def test_create_candidate_400_duplicate_request(self):
        new_candidatetest = {
            "idcandidate": self.data_factory.random_int(1, 500),
            "idtest": self.data_factory.random_int(1, 100)
        }
        resp_create = self.client.post(self.endpoint_create, headers = self.headers, data=json.dumps(new_candidatetest))
        #print(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 201)

        resp_create2 = self.client.post(self.endpoint_create, headers = self.headers, data=json.dumps(new_candidatetest))
        error_code2 = json.loads(resp_create2.get_data()).get('errorCode')
        self.assertEqual(error_code2, 'CO05')
        self.assertEqual(resp_create2.status_code, 400)
        
    def test_get_all_companies_200(self):
        resp_get = self.client.get(self.endpoint_create, headers = self.headers)
        #print(resp_get.get_data())
        self.assertEqual(resp_get.status_code, 200)

    def test_get_one_test_candidates(self):
        idcandidate = self.data_factory.random_int(1, 500)
        idtest = self.data_factory.random_int(1, 100)
        new_candidatetest = {
            "idcandidate": idcandidate,
            "idtest": idtest
        }
        resp_create = self.client.post(self.endpoint_create, headers = self.headers, data=json.dumps(new_candidatetest))
        #print(resp_create.get_data())
        endpoint_get = '/candidateTest/{}'.format(str(idcandidate)) 
        resp_get = self.client.get(endpoint_get, headers = self.headers)
        self.assertEqual(resp_get.status_code, 200)  

    def test_get_candidate_test_404(self):
        req_get = self.client.get(self.endpoint_get_404, headers = self.headers)
        #print(json.loads(req_get.get_data()))
        self.assertEqual(req_get.status_code, 404)

    def test_get_candidate_test_412(self):
        req_get = self.client.get(self.endpoint_get_412, headers = self.headers)
        #print(json.loads(req_get.get_data()))
        self.assertEqual(req_get.status_code, 412)

    def test_get_candidate_test_200(self):
        req_get = self.client.get(self.endpoint_get_200, headers = self.headers)
        #print(json.loads(req_get.get_data()))
        self.assertEqual(req_get.status_code, 200)

    def test_put_candidate_test_400(self):
        req_get = self.client.put(self.endpoint_get_200, headers = self.headers, data=json.dumps({}))
        #print(json.loads(req_get.get_data()))
        self.assertEqual(req_get.status_code, 400)

    def test_put_candidate_test_404(self):
        req_get = self.client.put(self.endpoint_get_404, headers = self.headers, data=json.dumps(self.data))
        #print(json.loads(req_get.get_data()))
        self.assertEqual(req_get.status_code, 404)

    def test_put_candidate_test_412(self):
        req_get = self.client.put(self.endpoint_get_412, headers = self.headers, data=json.dumps(self.data))
        #print(json.loads(req_get.get_data()))
        self.assertEqual(req_get.status_code, 412)

    def test_put_candidate_test_200(self):
        req_get = self.client.put(self.endpoint_get_200, headers = self.headers, data=json.dumps(self.data))
        #print(json.loads(req_get.get_data()))
        self.assertEqual(req_get.status_code, 200)
