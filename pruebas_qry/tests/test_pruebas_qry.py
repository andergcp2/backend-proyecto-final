import json, copy
from app import app
from model import db, Test, TechnicalSkill, Profile, Question, Answer
from faker import Faker
from unittest import TestCase
from unittest.mock import patch

class PruebasQry(TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.fake = Faker()
     
        self.token = "mangocat"
        self.headers_token = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        for x in range(2):
            new_test = Test(name=self.fake.job() +" "+ self.fake.bs(), numQuestions=self.fake.random_int(5, 10), minLevel=self.fake.random_int(1, 5)) 
            for y in range(2):
                new_test.profiles.append(Profile(profile=self.fake.job(), testId=new_test.id))
            for y in range(2):
                new_test.techSkills.append(TechnicalSkill(skill=self.fake.job(), testId=new_test.id))                
            for y in range(2):
                new_question = Question(question=self.fake.sentence(3), level=self.fake.random_int(1, 5), url=self.fake.url(), testId=new_test.id)
                for z in range(2):
                    new_answer = Answer(answer=self.fake.sentence(2), correct=False, questionId=new_question.id) 
                    new_question.answers.append(new_answer)
                new_test.questions.append(new_question)

            db.session.add(new_test)
            db.session.commit()
            test_created = Test.query.filter(Test.name == new_test.name).filter(Test.minLevel==new_test.minLevel).order_by(Test.createdAt.desc()).first()
            self.pruebaId = test_created.id


        self.endpoint_health = '/tests-qry/ping'
        self.endpoint_get = '/tests-qry'
        self.endpoint_get_200 = '/tests-qry/{}'.format(str(self.pruebaId))
        self.endpoint_get_404 = '/tests-qry/{}'.format(str(self.pruebaId * 1000))
        self.endpoint_get_412 = '/tests-qry/pruebaId'

    def test_health_check(self):
        req_health = self.client.get(self.endpoint_health, headers={'Content-Type': 'application/json'})
        self.assertEqual(req_health.status_code, 200)

    def test_get_prueba_404(self):
        req_get = self.client.get(self.endpoint_get_404, headers=self.headers_token)
        self.assertEqual(req_get.status_code, 404)

    def test_get_prueba_412(self):
        req_get = self.client.get(self.endpoint_get_412, headers=self.headers_token)
        self.assertEqual(req_get.status_code, 412)


    def test_get_prueba_200(self):
        req_get = self.client.get(self.endpoint_get_200, headers=self.headers_token)
        resp_get = json.loads(req_get.get_data())
        #print(self.pruebaId, resp_get["id"], resp_get["name"], resp_get["createdAt"])
        self.assertEqual(self.pruebaId, resp_get["id"])
        self.assertEqual(req_get.status_code, 200)

    def test_get_pruebas_200(self):
        req_get = self.client.get(self.endpoint_get, headers=self.headers_token)
        resp_get = json.loads(req_get.get_data())
        #print()
        #print(resp_get)
        self.assertEqual(req_get.status_code, 200)
