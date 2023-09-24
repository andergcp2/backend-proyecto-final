import json
from app import app
#from model import db, Prueba
from faker import Faker
from unittest import TestCase
from unittest.mock import patch

class TestPruebasOrquestador(TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.data_factory = Faker()
     
        self.token = "mangocat"
        self.headers_token = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        
        # prueba = Prueba(name='test-'+ self.data_factory.job() +'-'+ self.data_factory.company(), categoryId=self.data_factory.random_number(digits=2, fix_len=True))
        # db.session.add(prueba)
        # db.session.commit()
        # self.id_prueba = db.session.query(Prueba).filter(Prueba.name==prueba.name, Prueba.categoryId==prueba.categoryId).first().id
        #print(self.id_prueba, "=>", prueba.name, prueba.categoryId, prueba.createdAt)

        self.endpoint_health = '/pruebas-orquestador/ping'
        self.endpoint_init_400 = '/pruebas-orquestador/candidatoId/pruebaId'
        self.endpoint_init_404 = '/pruebas-orquestador/3600/9000'
        self.endpoint_init_200 = '/pruebas-orquestador/36/90'
        #self.endpoint_init_200 = '/pruebas-orquestador/{}/{}'.format(str(self.id_prueba), str(self.id_prueba))

    def test_health_check(self):
        req_health = self.client.get(self.endpoint_health, headers={'Content-Type': 'application/json'})
        self.assertEqual(req_health.status_code, 200)

    def test_init_prueba_404(self):
        req_get = self.client.post(self.endpoint_init_404, headers=self.headers_token)
        self.assertEqual(req_get.status_code, 404)
    '''        
    def test_init_prueba_400(self):
        req_get = self.client.post(self.endpoint_init_400, headers=self.headers_token)
        self.assertEqual(req_get.status_code, 400)

    def test_init_prueba_200(self):
        req_get = self.client.post(self.endpoint_init_200, headers=self.headers_token)
        resp_get = json.loads(req_get.get_data())
        #print(resp_get["id"], resp_get["name"], resp_get["categoryId"], resp_get["createdAt"])

        self.assertEqual(self.id_prueba, resp_get["id"])
        self.assertEqual(req_get.status_code, 200)
    '''    