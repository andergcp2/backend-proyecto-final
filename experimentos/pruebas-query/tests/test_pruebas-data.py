import json
from app import app
from model import db, Prueba
from faker import Faker
from unittest import TestCase
from unittest.mock import patch

class TestPruebasData(TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.data_factory = Faker()

    def test_health_check(self):
        num_pruebas = 3
        for x in range(num_pruebas):
            prueba = Prueba(name='test-'+ self.data_factory.word()+'-'+ self.data_factory.word(), categoryId=1)
            db.session.add(prueba)
            prueba = Prueba(name='test-'+ self.data_factory.word()+'-'+ self.data_factory.word(), categoryId=2)
            db.session.add(prueba)
            prueba = Prueba(name='test-'+ self.data_factory.word()+'-'+ self.data_factory.word(), categoryId=3)
            db.session.add(prueba)
        db.session.commit()
        self.assertEqual(num_pruebas, 3)
