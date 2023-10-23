import json
from app import app
from model import db, Candidate, TestCandidate
from faker import Faker
from unittest import TestCase
from unittest.mock import patch

class TestCandidatosQuery(TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.data_factory = Faker()
     
        self.token = "mangocat"
        self.headers_token = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        
        #self.id = self.data_factory.random_number(digits=3, fix_len=True)
        #self.username = self.data_factory.word()
        #self.token_validation_resp = {'msg': {"id": self.id, "username": self.username}, 'status_code': 200}

        candidate = Candidate(firstname=self.data_factory.first_name(), lastname=self.data_factory.last_name())
        db.session.add(candidate)
        db.session.commit()
        self.id_candidate = db.session.query(Candidate).filter(Candidate.firstname==candidate.firstname, Candidate.lastname==candidate.lastname).first().id
        #print(self.id_candidate, "=>", candidate.firstname, candidate.lastname, candidate.createdAt)

        self.endpoint_health = '/candidatos-query/ping'
        self.endpoint_get = '/candidatos-query'
        self.endpoint_get_400 = '/candidatos-query/id'
        self.endpoint_get_404 = '/candidatos-query/{}'.format(str(self.id_candidate * 100))
        self.endpoint_get_200 = '/candidatos-query/{}'.format(str(self.id_candidate))
        self.endpoint_get_tests_400 = '/candidatos-query/id/tests'
        self.endpoint_get_tests_404 = '/candidatos-query/{}/tests'.format(str(self.id_candidate * 100))
        self.endpoint_get_tests_200 = '/candidatos-query/{}/tests'.format(str(self.id_candidate))

    def test_health_check(self):
        req_health = self.client.get(self.endpoint_health, headers={'Content-Type': 'application/json'})
        #req_health.get_data()
        self.assertEqual(req_health.status_code, 200)

    def test_get_candidate_400(self):
        req_get = self.client.get(self.endpoint_get_400, headers=self.headers_token)
        self.assertEqual(req_get.status_code, 400)

    def test_get_candidate_404(self):
        req_get = self.client.get(self.endpoint_get_404, headers=self.headers_token)
        self.assertEqual(req_get.status_code, 404)

    def test_get_candidate_200(self):
        req_get = self.client.get(self.endpoint_get_200, headers=self.headers_token)
        resp_get = json.loads(req_get.get_data())
        #print(resp_get["id"], resp_get["firstname"], resp_get["lastname"], resp_get["createdAt"])

        self.assertEqual(self.id_candidate, resp_get["id"])
        self.assertEqual(req_get.status_code, 200)

    def test_get_tests_candidate_400(self):
        req_get = self.client.get(self.endpoint_get_tests_400, headers=self.headers_token)
        self.assertEqual(req_get.status_code, 400)

    def test_get_tests_candidate_404(self):
        req_get = self.client.get(self.endpoint_get_tests_404, headers=self.headers_token)
        self.assertEqual(req_get.status_code, 404)


    #@patch('view.validate_token')
    #def test_get_200(self, mock_token_validation):
    def test_get_tests_candidate_200(self):
        db.session.add(TestCandidate(id_candidate=self.id_candidate, id_test=self.data_factory.random_number(digits=3, fix_len=True)))
        db.session.add(TestCandidate(id_candidate=self.id_candidate, id_test=self.data_factory.random_number(digits=3, fix_len=True)))
        db.session.add(TestCandidate(id_candidate=self.id_candidate, id_test=self.data_factory.random_number(digits=3, fix_len=True)))
        db.session.commit()

        #mock_token_validation.return_value = self.token_validation_resp
        req_get = self.client.get(self.endpoint_get_tests_200, headers=self.headers_token)
        resp_get = json.loads(req_get.get_data())
        #print(resp_get[0]["id_candidate"], resp_get[0]["presented"], resp_get[0]["presentedAt"], resp_get[0]["result"], resp_get[0]["id_test"])
        #print(resp_get[1]["id_candidate"], resp_get[1]["presented"], resp_get[1]["presentedAt"], resp_get[1]["result"], resp_get[1]["id_test"])
        #print(resp_get[2]["id_candidate"], resp_get[2]["presented"], resp_get[2]["presentedAt"], resp_get[2]["result"], resp_get[2]["id_test"])

        self.assertEqual(self.id_candidate, resp_get[0]["id_candidate"])
        self.assertEqual(self.id_candidate, resp_get[1]["id_candidate"])        
        self.assertEqual(self.id_candidate, resp_get[2]["id_candidate"])
        self.assertEqual(req_get.status_code, 200)

    def test_get_preguntas_200(self):
        req_get = self.client.get(self.endpoint_get, headers=self.headers_token)
        resp_get = json.loads(req_get.get_data())
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
'''