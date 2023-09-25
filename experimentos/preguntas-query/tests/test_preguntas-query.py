import json
from app import app
from model import db, Pregunta, Respuesta
from faker import Faker
from unittest import TestCase
from unittest.mock import patch

class TestPreguntasQuery(TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.data_factory = Faker()
     
        self.token = "mangocat"
        self.headers_token = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        #self.id_prueba=self.data_factory.random_number(digits=3, fix_len=True)
        self.id_prueba=37
        # pregunta = Pregunta(pruebaId=self.id_prueba, description=self.data_factory.sentence())
        # db.session.add(pregunta)
        # db.session.commit()
        # self.id_pregunta = db.session.query(Pregunta).filter(Pregunta.pruebaId==self.id_prueba, Pregunta.description==pregunta.description).first().id
        self.id_pregunta = 1
        #print(self.id_pregunta, "=>", pregunta.pruebaId, pregunta.description)

        self.endpoint_health = '/preguntas-query/ping'
        self.endpoint_get = '/preguntas-query'
        self.endpoint_get_400 = '/preguntas-query/id'
        self.endpoint_get_404 = '/preguntas-query/{}'.format(str(self.id_pregunta * 10000))
        self.endpoint_get_200 = '/preguntas-query/{}'.format(str(self.id_pregunta))        
        self.endpoint_get_respuestas_400 = '/preguntas-query/id/respuestas'
        self.endpoint_get_respuestas_404 = '/preguntas-query/{}/respuestas'.format(str(self.id_pregunta * 10000))
        self.endpoint_get_respuestas_200 = '/preguntas-query/{}/respuestas'.format(str(self.id_pregunta))
        self.endpoint_get_preguntas_prueba_200 = '/preguntas-query/prueba/{}'.format(str(self.id_prueba))

    def test_health_check(self):
        req_health = self.client.get(self.endpoint_health, headers={'Content-Type': 'application/json'})
        self.assertEqual(req_health.status_code, 200)

    def test_get_pregunta_400(self):
        req_get = self.client.get(self.endpoint_get_400, headers=self.headers_token)
        self.assertEqual(req_get.status_code, 400)

    def test_get_pregunta_404(self):
        req_get = self.client.get(self.endpoint_get_404, headers=self.headers_token)
        self.assertEqual(req_get.status_code, 404)

    def test_get_pregunta_200(self):
        req_get = self.client.get(self.endpoint_get_200, headers=self.headers_token)
        resp_get = json.loads(req_get.get_data())
        #print(resp_get["id"], resp_get["pruebaId"], resp_get["description"])

        self.assertEqual(self.id_pregunta, resp_get["id"])
        self.assertEqual(req_get.status_code, 200)

    def test_get_respuestas_pregunta_400(self):
        req_get = self.client.get(self.endpoint_get_respuestas_400, headers=self.headers_token)
        self.assertEqual(req_get.status_code, 400)

    def test_get_respuestas_pregunta_404(self):
        req_get = self.client.get(self.endpoint_get_respuestas_404, headers=self.headers_token)
        self.assertEqual(req_get.status_code, 404)

    def test_get_preguntas_200(self):
        req_get = self.client.get(self.endpoint_get, headers=self.headers_token)
        resp_get = json.loads(req_get.get_data())
        self.assertEqual(req_get.status_code, 200)

    def test_get_preguntas_prueba_200(self):
        req_get = self.client.get(self.endpoint_get_preguntas_prueba_200, headers=self.headers_token)
        resp_get = json.loads(req_get.get_data())
        #print(resp_get)
        self.assertEqual(req_get.status_code, 200)
        
    '''
    def test_get_respuestas_pregunta_200(self):
        db.session.add(Respuesta(preguntaId=self.id_pregunta, description=self.data_factory.sentence()))
        db.session.add(Respuesta(preguntaId=self.id_pregunta, description=self.data_factory.sentence()))
        db.session.add(Respuesta(preguntaId=self.id_pregunta, description=self.data_factory.sentence()))
        db.session.add(Respuesta(preguntaId=self.id_pregunta, description=self.data_factory.sentence(), correct=True))
        db.session.commit()

        req_get = self.client.get(self.endpoint_get_respuestas_200, headers=self.headers_token)
        resp_get = json.loads(req_get.get_data())
        #print("")
        #print(resp_get[0]["preguntaId"], resp_get[0]["description"], resp_get[0]["correct"])
        #print(resp_get[1]["preguntaId"], resp_get[1]["description"], resp_get[1]["correct"])
        #print(resp_get[2]["preguntaId"], resp_get[2]["description"], resp_get[2]["correct"])
        #print(resp_get[3]["preguntaId"], resp_get[3]["description"], resp_get[3]["correct"])

        self.assertEqual(self.id_pregunta, resp_get[0]["preguntaId"])
        self.assertEqual(self.id_pregunta, resp_get[1]["preguntaId"])        
        self.assertEqual(self.id_pregunta, resp_get[2]["preguntaId"])
        self.assertEqual(self.id_pregunta, resp_get[3]["preguntaId"])
        self.assertEqual(req_get.status_code, 200)
    '''