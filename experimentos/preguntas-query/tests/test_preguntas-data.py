import json
from app import app
from model import db, Pregunta, Respuesta
from faker import Faker
from unittest import TestCase
from unittest.mock import patch

class TestCandidatosData(TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.data_factory = Faker()

    def test_health_check(self):
        questions = 300
        answers = 5
        id = 1

        for testId in range(37, 46):
            for x in range(questions):
                p = Pregunta(pruebaId=testId, description=self.data_factory.company() +" "+ self.data_factory.sentence())
                db.session.add(p)
                id = db.session.query(Pregunta).filter(Pregunta.pruebaId==p.pruebaId, Pregunta.description==p.description).first().id
                #print(id, p.pruebaId, p.description)

                for y in range(answers):
                    r = Respuesta(preguntaId=id, description=self.data_factory.word() +" "+ self.data_factory.word(), correct=False)
                    if(y==4):
                        r.correct=True
                    db.session.add(r)
                    #print("> ", y, r.preguntaId, r.description, r.correct)

        db.session.commit()
        self.assertEqual(questions, 300)
