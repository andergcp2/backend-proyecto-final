import json, copy
from app import app
from model import db, Test, TechnicalSkill, Profile, Question, Answer
from faker import Faker
from unittest import TestCase
from unittest.mock import patch

class PruebasCmd(TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.fake = Faker()
     
        self.token = "mangocat"
        self.headers_token = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        testProfiles = []
        for x in range(3):
            testProfiles.append({"profile": self.fake.job()})

        testTechSkills = []
        for x in range(6):
            testTechSkills.append({"skill": self.fake.word()})

        testQuestions = []
        for x in range(100):
            testQuestions.append(
                { 
                    "question": self.fake.sentence(6), 
                    "level": self.fake.random_int(1, 5), 
                    "url": self.fake.url(), 
                    "answers": [
                        {"answer": 'respuesta: '+ self.fake.sentence(3), "correct": False}, 
                        {"answer": 'respuesta: '+ self.fake.sentence(3), "correct": False}, 
                        {"answer": 'respuesta: '+ self.fake.sentence(3), "correct": False}, 
                        {"answer": 'respuesta: '+ self.fake.sentence(3), "correct": True}, 
                    ] 
                }
            )

        self.prueba = {
            "name": 'test '+ self.fake.job() +" "+ self.fake.bs(), 
            "numQuestions": self.fake.random_int(0, 50),
            "minLevel": self.fake.random_int(1, 5), 
            "profiles": testProfiles, 
            "techSkills": testTechSkills, 
            "questions": testQuestions,
        }
        #self.prueba = copy.deepcopy(self.test)
        
        self.endpoint = '/tests'
        self.endpoint_health = '/tests/ping'


    def test_health_check(self):
        req_health = self.client.get(self.endpoint_health, headers={'Content-Type': 'application/json'})
        self.assertEqual(req_health.status_code, 200)

    def test_create_test_400_name(self):
        self.prueba["name"] = None
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.prueba))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)

    def test_create_test_400_min_level(self):
        self.prueba["minLevel"] = None
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.prueba))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)

    def test_create_test_400_num_questions(self):
        self.prueba["numQuestions"] = None
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.prueba))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)

    def test_create_test_400_profiles(self):
        self.prueba["profiles"] = None
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.prueba))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)

    def test_create_test_400_tech_skills(self):
        self.prueba["techSkills"] = None
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.prueba))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)

    def test_create_test_400_questions(self):
        self.prueba["questions"] = None
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.prueba))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)

    def test_create_test_400_profiles_profile(self):
        self.prueba["profiles"] = [{"name": self.fake.job()}]
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.prueba))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)

    def test_create_test_400_techskills_skill(self):
        self.prueba["techSkills"] = [{"name": self.fake.word()}]
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.prueba))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)

    def test_create_test_400_questions_question(self):
        self.prueba["questions"] = [{"name": self.fake.word()}]
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.prueba))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)

    def test_create_test_400_questions_level(self):
        self.prueba["questions"] = [{"question": self.fake.word()}]
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.prueba))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)

    def test_create_test_400_questions_url(self):
        self.prueba["questions"] = [{"question": self.fake.word(), "level": self.fake.random_int(1, 5)}]
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.prueba))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)

    def test_create_test_400_questions_answers(self):
        self.prueba["questions"] = [{"question": self.fake.word(), "level": self.fake.random_int(1, 5), "url": self.fake.url()}]
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.prueba))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)

    def test_create_test_400_questions_answers_answer(self):
        self.prueba["questions"] = [{"question": self.fake.word(), "level": self.fake.random_int(1, 5), "url": self.fake.url(), "answers": [{"answerX": self.fake.sentence(2), "correct": False}]}]
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.prueba))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)

    def test_create_test_400_questions_answers_correct(self):
        self.prueba["questions"] = [{"question": self.fake.word(), "level": self.fake.random_int(1, 5), "url": self.fake.url(), "answers": [{"answer": self.fake.sentence(2), "correctX": False}]}]
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.prueba))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)

    def test_create_test_412_min_level(self):
        self.prueba["minLevel"] = self.fake.country_code()
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.prueba))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 412)

    def test_create_test_412_min_level_greater_than_5(self):
        self.prueba["minLevel"] = self.fake.random_int(6, 9)
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.prueba))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 412)

    def test_create_test_412_min_level_smaller_than_1(self):
        self.prueba["minLevel"] = self.fake.random_int(-3, 0)
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.prueba))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 412)

    def test_create_test_412_num_questions(self):
        self.prueba["numQuestions"] = self.fake.country_code()
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.prueba))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 412)

    def test_create_test_412_num_questions_greater_than_50(self):
        self.prueba["numQuestions"] = self.fake.random_int(51, 99)
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.prueba))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 412)

    def test_create_project_201(self):
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.prueba))
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 201)
        self.assertEqual(data["name"], self.prueba["name"])
        self.assertEqual(data["minLevel"], self.prueba["minLevel"])
        self.assertEqual(data["numQuestions"], self.prueba["numQuestions"])
