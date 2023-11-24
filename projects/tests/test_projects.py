import json
from app import app
from model import db, Project, Profile, SoftSkillProfile, TechSkillProfile, TestProfile
from faker import Faker
from unittest import TestCase
from unittest.mock import patch

class TestProjects(TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.fake = Faker()
     
        self.token = "mangocat"
        self.headers_token = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        
        techSkills = []
        softSkills = []
        tests = []
        profiles = []

        for x in range(3):
            techSkills.append({"id": self.fake.random_int(100, 299), "skill": self.fake.sentence(2)})
        for x in range(3):
            softSkills.append({"id": self.fake.random_int(300, 599), "skill": self.fake.sentence(2)})
        for x in range(3):
            tests.append({"id": self.fake.random_int(600, 999), "skill": self.fake.sentence(2)})
        for x in range(3):
            profiles.append(
                {
                    "name": self.fake.job(), 
                    "profession": self.fake.job(), 
                    "softskills": softSkills, 
                    "techskills": techSkills, 
                    "tests": tests, 
                }
            )

        self.project = {
            "name": self.fake.bs(), 
            "type": self.fake.android_platform_token(), 
            "leader": self.fake.name(), 
            "role": self.fake.job(), 
            "phone": self.fake.phone_number(), 
            "email": self.fake.company_email(), 
            "country": self.fake.country_code(), 
            "city": self.fake.random_int(10000, 99999), 
            "address": self.fake.street_address() +" "+ self.fake.street_name(), 
            "company": self.fake.random_int(1000, 9999),
            "profiles": profiles
        }

        self.candidato = {
            "id": self.fake.random_int(1000, 1999), 
            "name": self.fake.first_name(), 
            "lastName": self.fake.last_name(),
            "username": self.fake.email(),
            "softSkills": [{"skill": self.fake.word()}, {"skill": self.fake.word()}],
            "technicalSkills": [{"skill": self.fake.job()}, {"skill": self.fake.job()}],
            "createdAt": "2023-11-12T23:26:05.081973"
        }

        self.endpoint_health = '/projects/ping'
        self.endpoint = '/projects'
        self.endpoint_get_412 = '/projects/id'
        self.endpoint_get_404 = '/projects/{}'.format(self.fake.random_int(10, 99) * 0)
        self.endpoint_get_200 = '/projects/{}'.format(self.fake.random_int(10, 99))
        self.endpoint_get_tests_400 = '/projects/id/tests'
        self.endpoint_get_tests_404 = '/projects/{}/tests'.format(str(self.fake.random_int(10, 99) * 10))
        self.endpoint_get_projects_company_200 = '/projects/companies/{}'.format(self.project["company"])
        self.endpoint_get_projects_company_200_empty = '/projects/companies/{}'.format(self.project["company"]*10)

        self.endpoint_post_cand_proj_400_project = '/projects/projectId/candidates/candidatoId'
        self.endpoint_post_cand_proj_400_candidate = '/projects/0/candidates/candidatoId'
        self.endpoint_post_candidate_project_404 = '/projects/0/candidates/0'
        self.endpoint_post_candidate_project_201 = '/projects/{}/candidates/{}'.format(0, 0)

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

        resp_get = self.client.get(self.endpoint, headers=self.headers_token) #, data=json.dumps(self.project)
        data = json.loads(resp_get.get_data())
        self.assertEqual(resp_get.status_code, 200)

    def test_get_project_412(self):
        resp_get = self.client.get(self.endpoint_get_412, headers=self.headers_token)
        data = json.loads(resp_get.get_data())
        #print(self.endpoint_get_412, data)
        self.assertEqual(resp_get.status_code, 412)

    def test_get_project_404(self):
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.project))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 201)
        
        self.endpoint_get_404 = '/projects/{}'.format(data["id"]*10)
        resp_get = self.client.get(self.endpoint_get_404, headers=self.headers_token)
        data = json.loads(resp_get.get_data())
        #print(self.endpoint_get_404, data)
        self.assertEqual(resp_get.status_code, 404)

    def test_get_project_200(self):
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.project))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 201)
        
        self.endpoint_get_200 = '/projects/{}'.format(data["id"])
        resp_get = self.client.get(self.endpoint_get_200, headers=self.headers_token)
        data = json.loads(resp_get.get_data())
        # print()
        # print(print(json.dumps(data, indent=4)))
        self.assertEqual(resp_get.status_code, 200)

    def test_get_projects_company_200_empty(self):
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.project))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 201)

        req_get = self.client.get(self.endpoint_get_projects_company_200_empty, headers=self.headers_token)
        data = json.loads(req_get.get_data())
        self.assertEqual(req_get.status_code, 200)
        self.assertEqual(len(data), 0)

    def test_get_projects_company_200(self):
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.project))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 201)

        req_get = self.client.get(self.endpoint_get_projects_company_200, headers=self.headers_token)
        data = json.loads(req_get.get_data())
        self.assertEqual(req_get.status_code, 200)
        self.assertGreater(len(data), 0)

    def test_candidate_project_400(self):
        resp_create = self.client.post(self.endpoint_post_cand_proj_400_project, headers=self.headers_token)
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)

    def test_candidate_project_400_candidate(self):
        resp_create = self.client.post(self.endpoint_post_cand_proj_400_candidate, headers=self.headers_token)
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)

    def test_candidate_project_404_project(self):
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.project))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 201)

        self.endpoint_get_200 = '/projects/{}'.format(data["id"])
        resp_get = self.client.get(self.endpoint_get_200, headers=self.headers_token)
        data = json.loads(resp_get.get_data())
        self.assertEqual(resp_get.status_code, 200)

        self.endpoint_post_candidate_project_404 = '/projects/{}/candidates/0'.format(data["id"]*1000)
        resp_create = self.client.post(self.endpoint_post_candidate_project_404, headers=self.headers_token)
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 404)

    @patch('view.getCandidato')
    def test_candidate_project_404_candidate(self, mock_candidato):
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.project))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 201)

        self.endpoint_get_200 = '/projects/{}'.format(data["id"])
        resp_get = self.client.get(self.endpoint_get_200, headers=self.headers_token)
        data = json.loads(resp_get.get_data())
        self.assertEqual(resp_get.status_code, 200)

        self.endpoint_post_candidate_project_404 = '/projects/{}/candidates/0'.format(data["id"])
        mock_candidato.return_value = {'msg': 'candidato was not found by mango', 'status_code': 404}
        resp_create = self.client.post(self.endpoint_post_candidate_project_404, headers=self.headers_token)
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 404)        

    @patch('view.getCandidato')
    def test_candidate_project_201(self, mock_candidato):
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.project))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 201)

        self.endpoint_get_200 = '/projects/{}'.format(data["id"])
        resp_get = self.client.get(self.endpoint_get_200, headers=self.headers_token)
        data = json.loads(resp_get.get_data())
        self.assertEqual(resp_get.status_code, 200)

        self.endpoint_post_candidate_project_404 = '/projects/{}/candidates/{}'.format(data["id"], self.candidato["id"])
        mock_candidato.return_value = {'msg': self.candidato, 'status_code': 200}
        resp_create = self.client.post(self.endpoint_post_candidate_project_404, headers=self.headers_token)
        data = json.loads(resp_create.get_data())
        # print()
        # print(data)
        self.assertEqual(resp_create.status_code, 201)
