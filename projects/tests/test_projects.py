import json
from app import app
from model import db, Project, Profile, SkillProfile, TestProfile
from faker import Faker
from unittest import TestCase
from unittest.mock import patch

class TestProyectos(TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.fake = Faker()
     
        self.token = "mangocat"
        self.headers_token = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        
        #self.id = self.fake.random_number(digits=3, fix_len=True)
        #self.username = self.fake.word()
        #self.token_validation_resp = {'msg': {"id": self.id, "username": self.username}, 'status_code': 200}

        self.project = {
            "name": self.fake.bs(), 
            "type": self.fake.android_platform_token(), 
            "leader": self.fake.name(), 
            "role": self.fake.job(), 
            "phone": self.fake.phone_number(), 
            "email": self.fake.company_email(), 
            "country": self.fake.country_code(), 
            "city": self.fake.random_int(1, 99999), 
            "address": self.fake.street_address() +" "+ self.fake.street_name(), 
            "company": self.fake.random_int(1, 999),
            "profiles": [
                {
                    "name": self.fake.job(), 
                    "professional": self.fake.job(), 
                    "softskills": [
                        {"id": self.fake.random_int(100, 999), "name": self.fake.job()}, 
                        {"id": self.fake.random_int(100, 999), "name": self.fake.job()},                         
                        {"id": self.fake.random_int(100, 999), "name": self.fake.job()}
                    ], 
                    "techskills": [
                        {"id": self.fake.random_int(100, 999), "name": self.fake.job()}, 
                        {"id": self.fake.random_int(100, 999), "name": self.fake.job()}, 
                        {"id": self.fake.random_int(100, 999), "name": self.fake.job()}
                    ], 
                    "tests": [
                        {"id": self.fake.random_int(10, 99), "name": "Test "+ self.fake.job()}, 
                        {"id": self.fake.random_int(10, 99), "name": "Test "+ self.fake.job()},
                        {"id": self.fake.random_int(10, 99), "name": "Test "+ self.fake.job()}
                    ]
                }, 
                {
                    "name": self.fake.job(), 
                    "professional": self.fake.job(), 
                    "softskills": [
                        {"id": self.fake.random_int(100, 999), "name": self.fake.job()}, 
                        {"id": self.fake.random_int(100, 999), "name": self.fake.job()}, 
                        {"id": self.fake.random_int(100, 999), "name": self.fake.job()}
                    ], 
                    "techskills": [
                        {"id": self.fake.random_int(100, 999), "name": self.fake.job()}, 
                        {"id": self.fake.random_int(100, 999), "name": self.fake.job()}, 
                        {"id": self.fake.random_int(100, 999), "name": self.fake.job()}
                    ], 
                    "tests": [
                        {"id": self.fake.random_int(10, 99), "name": "Test "+ self.fake.job()}, 
                        {"id": self.fake.random_int(10, 99), "name": "Test "+ self.fake.job()}, 
                        {"id": self.fake.random_int(10, 99), "name": "Test "+ self.fake.job()}
                    ]
                }
            ]
        }

        self.endpoint_health = '/projects/ping'
        self.endpoint = '/projects'
        self.endpoint_get_400 = '/projects/id'
        self.endpoint_get_404 = '/projects/{}'.format(str(self.fake.random_int(10, 99) * 0))
        self.endpoint_get_200 = '/projects/{}'.format(str(self.fake.random_int(10, 99)))
        self.endpoint_get_tests_400 = '/projects/id/tests'
        self.endpoint_get_tests_404 = '/projects/{}/tests'.format(str(self.fake.random_int(10, 99) * 100))
        self.endpoint_get_tests_200 = '/projects/{}/tests'.format(str(self.fake.random_int(10, 99)))

    def test_health_check(self):
        req_health = self.client.get(self.endpoint_health, headers={'Content-Type': 'application/json'})
        #req_health.get_data()
        self.assertEqual(req_health.status_code, 200)

    def test_create_project_201(self):
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.project))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 201)
        self.assertEqual(data["name"], self.project["name"])
        self.assertEqual(data["leader"], self.project["leader"])
        self.assertEqual(data["companyId"], self.project["company"])

    def test_create_project_412(self):
        self.project["company"] = self.fake.country_code()
        self.project["city"] = self.fake.country_code()
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.project))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 412)

    def test_create_project_400(self):
        self.project["name"] = None
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.project))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)

    def test_get_projects_200(self):
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.project))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 201)

        resp_get = self.client.get(self.endpoint, headers=self.headers_token, data=json.dumps(self.project))
        data = json.loads(resp_get.get_data())
        self.assertEqual(resp_get.status_code, 200)

    # def test_get_project_404(self):
    #     resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.project))
    #     data = json.loads(resp_create.get_data())
    #     self.assertEqual(resp_create.status_code, 201)

    #     self.endpoint_get_404 = '/projects/{}'.format(data["id"]*10)
    #     resp_get = self.client.get(self.endpoint_get_404, headers=self.headers_token, data=json.dumps(self.project))
    #     data = json.loads(resp_get.get_data())
    #     #print(self.endpoint_get_404, data)
    #     self.assertEqual(resp_get.status_code, 404)

    # def test_get_project_200(self):
    #     resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.project))
    #     data = json.loads(resp_create.get_data())
    #     self.assertEqual(resp_create.status_code, 201)

    #     self.endpoint_get_200 = '/projects/{}'.format(data["id"])
    #     resp_get = self.client.get(self.endpoint_get_200, headers=self.headers_token, data=json.dumps(self.project))
    #     data = json.loads(resp_get.get_data())
    #     #print(self.endpoint_get_200)
    #     self.assertEqual(resp_get.status_code, 200)

    # def test_get_projects_404(self):
    #     req_get = self.client.get(self.endpoint_get_404, headers=self.headers_token)
    #     self.assertEqual(req_get.status_code, 404)

    # def test_get_projects_200(self):
    #     req_get = self.client.get(self.endpoint_get_200, headers=self.headers_token)
    #     resp_get = json.loads(req_get.get_data())
    #     #print(resp_get["id"], resp_get["firstname"], resp_get["lastname"], resp_get["createdAt"])

    #     self.assertEqual(self.id_candidate, resp_get["id"])
    #     self.assertEqual(req_get.status_code, 200)

    # def test_get_tests_candidate_400(self):
    #     req_get = self.client.get(self.endpoint_get_tests_400, headers=self.headers_token)
    #     self.assertEqual(req_get.status_code, 400)

    # def test_get_tests_candidate_404(self):
    #     req_get = self.client.get(self.endpoint_get_tests_404, headers=self.headers_token)
    #     self.assertEqual(req_get.status_code, 404)

    # def test_get_tests_candidate_200(self):
    #     db.session.add(TestCandidate(id_candidate=self.id_candidate, id_test=self.fake.random_number(digits=3, fix_len=True)))
    #     db.session.add(TestCandidate(id_candidate=self.id_candidate, id_test=self.fake.random_number(digits=3, fix_len=True)))
    #     db.session.add(TestCandidate(id_candidate=self.id_candidate, id_test=self.fake.random_number(digits=3, fix_len=True)))
    #     db.session.commit()

    #     req_get = self.client.get(self.endpoint_get_tests_200, headers=self.headers_token)
    #     resp_get = json.loads(req_get.get_data())

    #     self.assertEqual(self.id_candidate, resp_get[0]["id_candidate"])
    #     self.assertEqual(self.id_candidate, resp_get[1]["id_candidate"])        
    #     self.assertEqual(self.id_candidate, resp_get[2]["id_candidate"])
    #     self.assertEqual(req_get.status_code, 200)

    # def test_get_preguntas_200(self):
    #     req_get = self.client.get(self.endpoint_get, headers=self.headers_token)
    #     resp_get = json.loads(req_get.get_data())
    #     self.assertEqual(req_get.status_code, 200)
