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
            "phone": self.fake.phone_number(), 
            "email": self.fake.company_email(), 
            "username": self.fake.email(),
            "softSkills": [{"skill": self.fake.word()}, {"skill": self.fake.word()}],
            "technicalSkills": [{"skill": self.fake.job()}, {"skill": self.fake.job()}],
            "createdAt": "2023-11-12T23:26:05.081973"
        }

        self.evaluation = {
            "score": self.fake.random_int(1, 5),
            "comments": self.fake.sentence(), 
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

        self.endpoint_post_candidate_project_400_project = '/projects/projectId/candidates/candidatoId'
        self.endpoint_post_candidate_project_400_candidate = '/projects/0/candidates/candidatoId'
        self.endpoint_post_candidate_project_404 = '/projects/0/candidates/0'
        self.endpoint_post_candidate_project_201 = '/projects/{}/candidates/{}'.format(0, 0)
        
        self.endpoint_get_candidate_project_400 = '/projects/projectId/candidates'
        self.endpoint_get_candidate_project_404 = '/projects/0/candidates'
        self.endpoint_get_candidate_project_200 = '/projects/{}/candidates'.format(0)

        self.endpoint_evaluation = '/projects/{}/candidates/{}/evaluation'

    ''' '''
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
        resp_create = self.client.post(self.endpoint_post_candidate_project_400_project, headers=self.headers_token)
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)

    def test_candidate_project_400_candidate(self):
        resp_create = self.client.post(self.endpoint_post_candidate_project_400_candidate, headers=self.headers_token)
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

        self.endpoint_post_candidate_project_201 = '/projects/{}/candidates/{}'.format(data["id"], self.candidato["id"])
        mock_candidato.return_value = {'msg': self.candidato, 'status_code': 200}
        resp_create = self.client.post(self.endpoint_post_candidate_project_201, headers=self.headers_token)
        data = json.loads(resp_create.get_data())
        # print(data)
        self.assertEqual(resp_create.status_code, 201)

    def test_get_candidate_project_400(self):
        resp_create = self.client.get(self.endpoint_get_candidate_project_400, headers=self.headers_token)
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)

    def test_get_candidate_project_404_project(self):
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.project))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 201)

        self.endpoint_get_200 = '/projects/{}'.format(data["id"])
        resp_get = self.client.get(self.endpoint_get_200, headers=self.headers_token)
        data = json.loads(resp_get.get_data())
        self.assertEqual(resp_get.status_code, 200)

        self.endpoint_get_candidate_project_404 = '/projects/{}/candidates'.format(data["id"]*1000)
        resp_create = self.client.get(self.endpoint_get_candidate_project_404, headers=self.headers_token)
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 404)

    @patch('view.getCandidato')
    @patch('view.getCandidato')    
    def test_get_candidate_project_412(self, mock_candidato2, mock_candidato):
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.project))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 201)

        self.endpoint_get_200 = '/projects/{}'.format(data["id"])
        resp_get = self.client.get(self.endpoint_get_200, headers=self.headers_token)
        data = json.loads(resp_get.get_data())
        self.assertEqual(resp_get.status_code, 200)

        self.endpoint_post_candidate_project_201 = '/projects/{}/candidates/{}'.format(data["id"], self.candidato["id"])
        mock_candidato.return_value = {'msg': self.candidato, 'status_code': 200}
        resp_create = self.client.post(self.endpoint_post_candidate_project_201, headers=self.headers_token)
        data = json.loads(resp_create.get_data())
        #print(data)
        self.assertEqual(resp_create.status_code, 201)

        mock_candidato2.return_value = {'msg': self.candidato, 'status_code': 200}
        resp_create = self.client.post(self.endpoint_post_candidate_project_201, headers=self.headers_token)
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 412)

    @patch('view.getCandidato')
    @patch('view.getCandidato')
    def test_get_candidate_project_200(self, mock_candidato2, mock_candidato):
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.project))
        data = json.loads(resp_create.get_data())
        # print()
        # print("init: ", data['id'], data['name'])
        self.assertEqual(resp_create.status_code, 201)

        self.endpoint_get_200 = '/projects/{}'.format(data["id"])
        resp_get = self.client.get(self.endpoint_get_200, headers=self.headers_token)
        data = json.loads(resp_get.get_data())
        # print(" get: ", data['id'], data['name'])
        self.assertEqual(resp_get.status_code, 200)

        self.endpoint_post_candidate_project_201 = '/projects/{}/candidates/{}'.format(data["id"], self.candidato["id"])
        mock_candidato.return_value = {'msg': self.candidato, 'status_code': 200}
        resp_create = self.client.post(self.endpoint_post_candidate_project_201, headers=self.headers_token)
        data = json.loads(resp_create.get_data())
        # print(" set: ", data['projectId'], data['candidateId'])
        self.assertEqual(resp_create.status_code, 201)

        mock_candidato2.return_value = {'msg': self.candidato, 'status_code': 200}
        self.endpoint_get_candidate_project_200 = '/projects/{}/candidates'.format(data["projectId"])
        resp_create = self.client.get(self.endpoint_get_candidate_project_200, headers=self.headers_token)
        data = json.loads(resp_create.get_data())
        cand = json.loads(data[0])
        # print("done: ", type(data), len(data), type(cand), cand)
        # print("done: ", self.candidato['id'], cand['id'], cand['name'])
        self.assertEqual(resp_create.status_code, 200)
        self.assertGreater(len(data), 0)
        self.assertEqual(cand['id'], self.candidato['id'])
    ''' '''

    def test_post_evaluation_400_project(self):
        self.endpoint_evaluation = self.endpoint_evaluation.format('projectId', 0)
        resp = self.client.post(self.endpoint_evaluation, headers=self.headers_token, data=json.dumps(self.evaluation))
        data = json.loads(resp.get_data())
        #print(data)
        self.assertEqual(resp.status_code, 400)

    def test_post_evaluation_400_candidate(self):
        self.endpoint_evaluation = self.endpoint_evaluation.format(0, 'candidatoId')
        resp = self.client.post(self.endpoint_evaluation, headers=self.headers_token, data=json.dumps(self.evaluation))
        data = json.loads(resp.get_data())
        #print(data)
        self.assertEqual(resp.status_code, 400)

    def test_post_evaluation_400_score_required(self):
        self.evaluation = {}
        self.endpoint_evaluation = self.endpoint_evaluation.format(0, 0)
        resp = self.client.post(self.endpoint_evaluation, headers=self.headers_token, data=json.dumps(self.evaluation))
        data = json.loads(resp.get_data())
        #print(data)
        self.assertEqual(resp.status_code, 400)

    def test_post_evaluation_400_comments_required(self):
        #self.evaluation["comments"] = None
        self.evaluation = {"score": self.fake.random_int(1, 5)}
        self.endpoint_evaluation = self.endpoint_evaluation.format(0, 0)
        resp = self.client.post(self.endpoint_evaluation, headers=self.headers_token, data=json.dumps(self.evaluation))
        data = json.loads(resp.get_data())
        #print(data)
        self.assertEqual(resp.status_code, 400)

    def test_post_evaluation_412_score_not_int(self):
        self.evaluation["score"] = self.fake.word()
        self.endpoint_evaluation = self.endpoint_evaluation.format(0, 0)
        resp = self.client.post(self.endpoint_evaluation, headers=self.headers_token, data=json.dumps(self.evaluation))
        data = json.loads(resp.get_data())
        #print(data)
        self.assertEqual(resp.status_code, 412)

    def test_post_evaluation_412_score_range_sup(self):
        self.evaluation["score"] = self.fake.random_int(6, 9)
        self.endpoint_evaluation = self.endpoint_evaluation.format(0, 0)
        resp = self.client.post(self.endpoint_evaluation, headers=self.headers_token, data=json.dumps(self.evaluation))
        data = json.loads(resp.get_data())
        #print(data)
        self.assertEqual(resp.status_code, 412)

    def test_post_evaluation_412_score_range_inf(self):
        self.evaluation["score"] = self.fake.random_int(-9, -1)
        self.endpoint_evaluation = self.endpoint_evaluation.format(0, 0)
        resp = self.client.post(self.endpoint_evaluation, headers=self.headers_token, data=json.dumps(self.evaluation))
        data = json.loads(resp.get_data())
        #print(data)
        self.assertEqual(resp.status_code, 412)

    def test_post_evaluation_404_project(self):
        self.endpoint_evaluation = self.endpoint_evaluation.format(self.fake.random_int(100000, 999999), 0)
        resp = self.client.post(self.endpoint_evaluation, headers=self.headers_token, data=json.dumps(self.evaluation))
        data = json.loads(resp.get_data())
        #print(data)
        self.assertEqual(resp.status_code, 404)

    def test_post_evaluation_412_project(self):
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.project))
        data = json.loads(resp_create.get_data())
        # print("init: ", data['id'], data['name'])
        projectId = data['id']
        self.assertEqual(resp_create.status_code, 201)

        self.endpoint_get_200 = '/projects/{}'.format(data["id"])
        resp_get = self.client.get(self.endpoint_get_200, headers=self.headers_token)
        data = json.loads(resp_get.get_data())
        # print(" get: ", data['id'], data['name'])
        self.assertEqual(resp_get.status_code, 200)

        self.endpoint_evaluation = self.endpoint_evaluation.format(projectId, self.fake.random_int(100000, 999999))
        resp = self.client.post(self.endpoint_evaluation, headers=self.headers_token, data=json.dumps(self.evaluation))
        data = json.loads(resp.get_data())
        # print("eval:", data)
        self.assertEqual(resp.status_code, 412)

    @patch('view.getCandidato')
    def test_post_evaluation_412_evaluated(self, mock_candidato):
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.project))
        data = json.loads(resp_create.get_data())
        # print("init: ", data['id'], data['name'])
        projectId = data['id']
        self.assertEqual(resp_create.status_code, 201)

        self.endpoint_get_200 = '/projects/{}'.format(data["id"])
        resp_get = self.client.get(self.endpoint_get_200, headers=self.headers_token)
        data = json.loads(resp_get.get_data())
        # print(" get: ", data['id'], data['name'])
        self.assertEqual(resp_get.status_code, 200)

        self.endpoint_post_candidate_project_201 = '/projects/{}/candidates/{}'.format(data["id"], self.candidato["id"])
        mock_candidato.return_value = {'msg': self.candidato, 'status_code': 200}
        resp_create = self.client.post(self.endpoint_post_candidate_project_201, headers=self.headers_token)
        data = json.loads(resp_create.get_data())
        # print(" set:", data['projectId'], data['candidateId'])
        self.assertEqual(resp_create.status_code, 201)

        self.endpoint_evaluation = self.endpoint_evaluation.format(projectId, self.candidato["id"])
        resp = self.client.post(self.endpoint_evaluation, headers=self.headers_token, data=json.dumps(self.evaluation))
        data = json.loads(resp.get_data())
        # print("eval:", data['projectId'], data['candidateId'], data['createdAt'])
        self.assertEqual(resp.status_code, 201)

        self.endpoint_evaluation = self.endpoint_evaluation.format(projectId, self.candidato["id"])
        resp = self.client.post(self.endpoint_evaluation, headers=self.headers_token, data=json.dumps(self.evaluation))
        data = json.loads(resp.get_data())
        # print("eval:", data)
        self.assertEqual(resp.status_code, 412)

    @patch('view.getCandidato')
    def test_post_evaluation_201(self, mock_candidato):
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.project))
        data = json.loads(resp_create.get_data())
        # print("init: ", data['id'], data['name'])
        projectId = data['id']
        self.assertEqual(resp_create.status_code, 201)

        self.endpoint_get_200 = '/projects/{}'.format(data["id"])
        resp_get = self.client.get(self.endpoint_get_200, headers=self.headers_token)
        data = json.loads(resp_get.get_data())
        # print(" get: ", data['id'], data['name'])
        self.assertEqual(resp_get.status_code, 200)

        self.endpoint_post_candidate_project_201 = '/projects/{}/candidates/{}'.format(data["id"], self.candidato["id"])
        mock_candidato.return_value = {'msg': self.candidato, 'status_code': 200}
        resp_create = self.client.post(self.endpoint_post_candidate_project_201, headers=self.headers_token)
        data = json.loads(resp_create.get_data())
        # print(" set:", data['projectId'], data['candidateId'])
        self.assertEqual(resp_create.status_code, 201)

        self.endpoint_evaluation = self.endpoint_evaluation.format(projectId, self.candidato["id"])
        resp = self.client.post(self.endpoint_evaluation, headers=self.headers_token, data=json.dumps(self.evaluation))
        data = json.loads(resp.get_data())
        #print("eval:", data['projectId'], data['candidateId'], data['score'], data['createdAt'])
        self.assertEqual(resp.status_code, 201)
