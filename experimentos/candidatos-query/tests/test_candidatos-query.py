import json
from app import app
from model import db, Candidate, CandidateTest
from faker import Faker
from unittest import TestCase
from unittest.mock import patch

class TestCandidatosQuery(TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.data_factory = Faker()
     
        self.token = "t0k3n"
        self.headers_token = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        
        self.id = self.data_factory.random_number(digits=3, fix_len=True)
        self.username = self.data_factory.word()
        self.token_validation_resp = {'msg': {"id": self.id, "username": self.username}, 'status_code': 200}

        candidate = Candidate(firstname=self.name(), lastname=self.data_factory.word())
        db.session.add(candidate)
        self.id_candidate = db.session.query(Candidate).filter(Candidate.firstname==candidate.firstname, Candidate.lastname==candidate.lastname).first()

        testid = self.data_factory.random_number(digits=3, fix_len=True))
        db.session.add(candidateTestTestCandidate(id_candidate=self.id_candidate, id_test=testid)

        testid = self.data_factory.random_number(digits=3, fix_len=True))
        db.session.add(candidateTestTestCandidate(id_candidate=self.id_candidate, id_test=testid)

        testid = self.data_factory.random_number(digits=3, fix_len=True))
        db.session.add(candidateTestTestCandidate(id_candidate=self.id_candidate, id_test=testid)
        db.session.commit() 

        self.endpoint_health = '/candidates-query/ping'
        self.endpoint_get = '/candidates-query/{}/tests/'.format(str(self.id_candidate)) 


    def test_health(self):
        req_health = self.client.get(self.endpoint_health, headers={'Content-Type': 'application/json'})
        json.loads(req_health.get_data())
        self.assertEqual(req_health.status_code, 200)


    #@patch('view.validate_token')
    #def test_get_200(self, mock_token_validation):
    def test_get_200(self):

        #mock_token_validation.return_value = self.token_validation_resp
        req_get = self.client.get(self.endpoint_get, headers=self.headers_token)
        resp_get = json.loads(req_get.get_data())
        print(resp_get)
        #self.assertEqual(new_offer["postId"], resp_get["postId"])
        #self.assertEqual(new_offer["offer"], resp_get["offer"])
        self.assertEqual(req_get.status_code, 200)
'''
    #@patch('view.validate_token')
    def test_get_404(self, mock_token_validation):
        new_offer = {
            "postId": self.data_factory.random_number(digits=3, fix_len=True),
            "description": self.data_factory.text(),
            "size": "MEDIUM",
            "fragile": True, #self.data_factory.boolean,
            "offer": self.data_factory.random_number(digits=3, fix_len=True)
        }
        mock_token_validation.return_value = self.token_validation_resp
        req_create = self.client.post(self.endpoint, data=json.dumps(new_offer), headers=self.headers_token)
        resp_create = json.loads(req_create.get_data())
        self.assertEqual(req_create.status_code, 201)

        endpoint_get = '/offers/{}000'.format(str(resp_create["id"])) 
        req_get = self.client.get(endpoint_get, headers=self.headers_token)
        json.loads(req_get.get_data())
        self.assertEqual(req_get.status_code, 404)

    #@patch('view.validate_token')
    def test_get_400(self, mock_token_validation):
        mock_token_validation.return_value = self.token_validation_resp
        endpoint_get = '/offers/{}'.format("test") 
        req_get = self.client.get(endpoint_get, headers=self.headers_token)
        req_get.get_data()
        self.assertEqual(req_get.status_code, 400)
'''
