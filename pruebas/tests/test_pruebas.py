import json
from app import app
from model import db, Test, TechnicalSkill, Profile, Question, Answer
from faker import Faker
from unittest import TestCase
from unittest.mock import patch

class TestPruebasCmd(TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.fake = Faker()
     
        self.token = "mangocat"
        self.headers_token = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        self.prueba = {
            "name": 'test '+ self.fake.job() +" "+ self.fake.bs(), 
            "numQuestions": self.fake.random_int(10, 25),
            "minLevel": self.fake.random_int(1, 5), 
            "profiles": [
                {
                    "profile": self.fake.job()
                }, 
                {
                    "profile": self.fake.job()
                } 
            ],
            "techSkills": [
                {
                    "skill": self.fake.word()
                }, 
                {
                    "skill": self.fake.word()
                } 
            ], 
            "questions": [
                {
                    "question": 'pregunta: '+ self.fake.sentence(8),
                    "level": self.fake.random_int(1, 5),
                    "url": self.fake.url(), 
                    "answers": [
                        {"answer": 'respuesta: '+ self.fake.sentence(3), "correct": False}, 
                        {"answer": 'respuesta: '+ self.fake.sentence(4), "correct": False}, 
                        {"answer": 'respuesta: '+ self.fake.sentence(5), "correct": False}, 
                        {"answer": 'respuesta: '+ self.fake.sentence(6), "correct": True}, 
                    ], 
                }, 
                {
                    "question": 'pregunta: '+ self.fake.sentence(6),
                    "level": self.fake.random_int(1, 5),
                    "url": self.fake.url(), 
                    "answers": [
                        {"answer": 'respuesta: '+ self.fake.sentence(3), "correct": False}, 
                        {"answer": 'respuesta: '+ self.fake.sentence(4), "correct": False}, 
                        {"answer": 'respuesta: '+ self.fake.sentence(5), "correct": False}, 
                        {"answer": 'respuesta: '+ self.fake.sentence(6), "correct": True}, 
                    ], 
                }
            ]
        }

        self.endpoint = '/tests'
        self.endpoint_health = '/tests/ping'


    def test_health_check(self):
        req_health = self.client.get(self.endpoint_health, headers={'Content-Type': 'application/json'})
        self.assertEqual(req_health.status_code, 200)
