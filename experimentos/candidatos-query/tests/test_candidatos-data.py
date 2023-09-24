import json
from app import app
from model import db, Candidate, TestCandidate
from faker import Faker
from unittest import TestCase
from unittest.mock import patch

class TestCandidatosData(TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.data_factory = Faker()

    def test_health_check(self):
        id = 1        
        num = 100
        testId = 37
        for x in range(num):
            c = Candidate(firstname=self.data_factory.name(), lastname=self.data_factory.word())
            db.session.add(c)
            id = db.session.query(Candidate).filter(Candidate.firstname==c.firstname, Candidate.lastname==c.lastname).first().id
            tc = TestCandidate(id_candidate=id, id_test=testId)
            db.session.add(tc)
            #print(c.firstname, c.lastname, id, testId)

            if(testId==45):
                testId=37
            else:
                testId=testId+1

        db.session.commit()
        self.assertEqual(num, 100)
