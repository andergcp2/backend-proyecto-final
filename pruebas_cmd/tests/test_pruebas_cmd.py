import io, copy, json
from app import app
from faker import Faker
from unittest import TestCase
from unittest.mock import patch
from werkzeug.datastructures import FileStorage
from model import db, Test, TechnicalSkill, Profile, Question, Answer

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
        for x in range(3):
            testTechSkills.append({"skill": self.fake.word()})

        testQuestions = []
        for x in range(9):
            testQuestions.append(
                { 
                    "question": self.fake.sentence(3), 
                    "level": self.fake.random_int(1, 5), 
                    "url": self.fake.url(), 
                    "answers": [
                        {"answer": self.fake.sentence(2), "correct": False}, 
                        {"answer": self.fake.sentence(2), "correct": False}, 
                        {"answer": self.fake.sentence(2), "correct": True}, 
                    ] 
                }
            )

        self.prueba = {
            "name": self.fake.job() +" "+ self.fake.bs(), 
            "numQuestions": self.fake.random_int(0, 50),
            "minLevel": self.fake.random_int(1, 5), 
            "profiles": testProfiles, 
            "techSkills": testTechSkills, 
            "questions": testQuestions,
        }
        #self.prueba = copy.deepcopy(self.test)
        
        self.data = {}
        self.endpoint = '/tests'
        self.endpoint_health = '/tests/ping'

    def test_health_check(self):
        req_health = self.client.get(self.endpoint_health, headers={'Content-Type': 'application/json'})
        self.assertEqual(req_health.status_code, 200)

    def test_create_test_400_file_missing(self):
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, data=json.dumps(self.prueba)) 
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)
        self.assertEqual(data, "Test was not created - file missing")

    def test_create_test_400_no_selected_file(self):
        input_json = json.dumps({}, indent=4).encode("utf-8")        
        self.data['file'] = FileStorage( stream=io.BytesIO(input_json), content_type="application/json", filename='') 
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, content_type='multipart/form-data', data=self.data) # follow_redirects=True
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)
        self.assertEqual(data, "Test was not created - no selected file")

    def test_create_test_400_extension_unsopported(self):
        input_json = json.dumps(self.prueba, indent=4).encode("utf-8")
        self.data['file'] = FileStorage( stream=io.BytesIO(input_json), content_type="application/json", filename="test.csv", )
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, content_type='multipart/form-data', data=self.data) # follow_redirects=True
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)
        self.assertEqual(data, "Test was not created - extension not supported")

    def test_create_test_400_name(self):
        self.prueba["name"] = None
        input_json = json.dumps(self.prueba, indent=4).encode("utf-8")
        self.data['file'] = FileStorage( stream=io.BytesIO(input_json), content_type="application/json", filename="test.json", )
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, content_type='multipart/form-data', data=self.data) # follow_redirects=True
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)
        self.assertEqual(data, "Test was not created - name is required")

    def test_create_test_400_min_level(self):
        self.prueba["minLevel"] = None
        input_json = json.dumps(self.prueba, indent=4).encode("utf-8")
        self.data['file'] = FileStorage( stream=io.BytesIO(input_json), content_type="application/json", filename="test.json", )
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, content_type='multipart/form-data', data=self.data) # follow_redirects=True
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)
        self.assertEqual(data, "Test was not created - minimun level is required")

    def test_create_test_400_num_questions(self):
        self.prueba["numQuestions"] = None
        input_json = json.dumps(self.prueba, indent=4).encode("utf-8")
        self.data['file'] = FileStorage( stream=io.BytesIO(input_json), content_type="application/json", filename="test.json", )
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, content_type='multipart/form-data', data=self.data) # follow_redirects=True
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)
        self.assertEqual(data, "Test was not created - number of questions is required")

    def test_create_test_400_profiles(self):
        self.prueba["profiles"] = None
        input_json = json.dumps(self.prueba, indent=4).encode("utf-8")
        self.data['file'] = FileStorage( stream=io.BytesIO(input_json), content_type="application/json", filename="test.json", )
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, content_type='multipart/form-data', data=self.data) # follow_redirects=True
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)
        self.assertEqual(data, "Test was not created - profiles are required")

    def test_create_test_400_tech_skills(self):
        self.prueba["techSkills"] = None
        input_json = json.dumps(self.prueba, indent=4).encode("utf-8")
        self.data['file'] = FileStorage( stream=io.BytesIO(input_json), content_type="application/json", filename="test.json", )
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, content_type='multipart/form-data', data=self.data) # follow_redirects=True
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)
        self.assertEqual(data, "Test was not created - technical skills are required")

    def test_create_test_400_questions(self):
        self.prueba["questions"] = None
        input_json = json.dumps(self.prueba, indent=4).encode("utf-8")
        self.data['file'] = FileStorage( stream=io.BytesIO(input_json), content_type="application/json", filename="test.json", )
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, content_type='multipart/form-data', data=self.data) # follow_redirects=True
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)
        self.assertEqual(data, "Test was not created - questions are required")

    def test_create_test_400_profiles_profile(self):
        self.prueba["profiles"] = [{"name": self.fake.job()}]
        input_json = json.dumps(self.prueba, indent=4).encode("utf-8")
        self.data['file'] = FileStorage( stream=io.BytesIO(input_json), content_type="application/json", filename="test.json", )
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, content_type='multipart/form-data', data=self.data) # follow_redirects=True
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)
        self.assertEqual(data, "Test was not created - profile is required")
    
    def test_create_test_400_techskills_skill(self):
        self.prueba["techSkills"] = [{"name": self.fake.word()}]
        input_json = json.dumps(self.prueba, indent=4).encode("utf-8")
        self.data['file'] = FileStorage( stream=io.BytesIO(input_json), content_type="application/json", filename="test.json", )
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, content_type='multipart/form-data', data=self.data) # follow_redirects=True
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)
        self.assertEqual(data, "Test was not created - skill is required")

    def test_create_test_400_questions_question(self):
        self.prueba["questions"] = [{"name": self.fake.word()}]
        input_json = json.dumps(self.prueba, indent=4).encode("utf-8")
        self.data['file'] = FileStorage( stream=io.BytesIO(input_json), content_type="application/json", filename="test.json", )
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, content_type='multipart/form-data', data=self.data) # follow_redirects=True
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)
        self.assertEqual(data, "Test was not created - question is required")

    def test_create_test_400_questions_level(self):
        self.prueba["questions"] = [{"question": self.fake.word()}]
        input_json = json.dumps(self.prueba, indent=4).encode("utf-8")
        self.data['file'] = FileStorage( stream=io.BytesIO(input_json), content_type="application/json", filename="test.json", )
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, content_type='multipart/form-data', data=self.data) # follow_redirects=True
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)
        self.assertEqual(data, "Test was not created - level's question is required")

    def test_create_test_400_questions_url(self):
        self.prueba["questions"] = [{"question": self.fake.word(), "level": self.fake.random_int(1, 5)}]
        input_json = json.dumps(self.prueba, indent=4).encode("utf-8")
        self.data['file'] = FileStorage( stream=io.BytesIO(input_json), content_type="application/json", filename="test.json", )
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, content_type='multipart/form-data', data=self.data) # follow_redirects=True
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)
        self.assertEqual(data, "Test was not created - url's question is required")

    def test_create_test_400_questions_answers(self):
        self.prueba["questions"] = [{"question": self.fake.word(), "level": self.fake.random_int(1, 5), "url": self.fake.url()}]
        input_json = json.dumps(self.prueba, indent=4).encode("utf-8")
        self.data['file'] = FileStorage( stream=io.BytesIO(input_json), content_type="application/json", filename="test.json", )
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, content_type='multipart/form-data', data=self.data) # follow_redirects=True        data = json.loads(resp_create.get_data())
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)
        self.assertEqual(data, "Test was not created - answers' question are required")

    def test_create_test_400_questions_answers_answer(self):
        self.prueba["questions"] = [{"question": self.fake.word(), "level": self.fake.random_int(1, 5), "url": self.fake.url(), "answers": [{"answerX": self.fake.sentence(2), "correct": False}]}]
        input_json = json.dumps(self.prueba, indent=4).encode("utf-8")
        self.data['file'] = FileStorage( stream=io.BytesIO(input_json), content_type="application/json", filename="test.json", )
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, content_type='multipart/form-data', data=self.data) # follow_redirects=True
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)
        self.assertEqual(data, "Test was not created - answer is required")

    def test_create_test_400_questions_answers_correct(self):
        self.prueba["questions"] = [{"question": self.fake.word(), "level": self.fake.random_int(1, 5), "url": self.fake.url(), "answers": [{"answer": self.fake.sentence(2), "correctX": False}]}]
        input_json = json.dumps(self.prueba, indent=4).encode("utf-8")
        self.data['file'] = FileStorage( stream=io.BytesIO(input_json), content_type="application/json", filename="test.json", )
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, content_type='multipart/form-data', data=self.data) # follow_redirects=True
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 400)
        self.assertEqual(data, "Test was not created - correctness' answer is required")

    def test_create_test_412_min_level(self):
        self.prueba["minLevel"] = self.fake.country_code()
        input_json = json.dumps(self.prueba, indent=4).encode("utf-8")
        self.data['file'] = FileStorage( stream=io.BytesIO(input_json), content_type="application/json", filename="test.json", )
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, content_type='multipart/form-data', data=self.data) # follow_redirects=True
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 412)
        self.assertEqual(data, "Test was not created - minimum level is not valid")

    def test_create_test_412_min_level_greater_than_5(self):
        self.prueba["minLevel"] = self.fake.random_int(6, 9)
        input_json = json.dumps(self.prueba, indent=4).encode("utf-8")
        self.data['file'] = FileStorage( stream=io.BytesIO(input_json), content_type="application/json", filename="test.json", )
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, content_type='multipart/form-data', data=self.data) # follow_redirects=True
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 412)
        self.assertEqual(data, "Test was not created - minimum level is not valid")

    def test_create_test_412_min_level_smaller_than_1(self):
        self.prueba["minLevel"] = self.fake.random_int(-3, 0)
        input_json = json.dumps(self.prueba, indent=4).encode("utf-8")
        self.data['file'] = FileStorage( stream=io.BytesIO(input_json), content_type="application/json", filename="test.json", )
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, content_type='multipart/form-data', data=self.data) # follow_redirects=True
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 412)
        self.assertEqual(data, "Test was not created - minimum level is not valid")

    def test_create_test_412_num_questions(self):
        self.prueba["numQuestions"] = self.fake.country_code()
        input_json = json.dumps(self.prueba, indent=4).encode("utf-8")
        self.data['file'] = FileStorage( stream=io.BytesIO(input_json), content_type="application/json", filename="test.json", )
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, content_type='multipart/form-data', data=self.data) # follow_redirects=True
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 412)
        self.assertEqual(data, "Test was not created - number of questions is not valid")

    def test_create_test_412_num_questions_greater_than_50(self):
        self.prueba["numQuestions"] = self.fake.random_int(51, 99)
        input_json = json.dumps(self.prueba, indent=4).encode("utf-8")
        self.data['file'] = FileStorage( stream=io.BytesIO(input_json), content_type="application/json", filename="test.json", )
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, content_type='multipart/form-data', data=self.data) # follow_redirects=True
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 412)
        self.assertEqual(data, "Test was not created - number of questions is not valid")

    def test_create_test_201(self):
        print()
        print(json.dumps(self.prueba, indent=4))
        input_json = json.dumps(self.prueba, indent=4).encode("utf-8") #sort_keys=True, indent=4
        self.data['file'] = FileStorage( stream=io.BytesIO(input_json), content_type="application/json", filename="test.json", )
        resp_create = self.client.post(self.endpoint, headers=self.headers_token, content_type='multipart/form-data', data=self.data) # follow_redirects=True
        data = json.loads(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 201)
        self.assertEqual(data["name"], self.prueba["name"])
        self.assertEqual(data["minLevel"], self.prueba["minLevel"])
        self.assertEqual(data["numQuestions"], self.prueba["numQuestions"])
