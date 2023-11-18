import json
from unittest import TestCase
from app import app
from faker import Faker
from modelos import db, Candidate, SoftSkills, TechnicalSkills


class TestCandidates(TestCase):
    """Class for test service"""

    def setUp(self):
        self.client = app.test_client()
        self.fake = Faker()

        for x in range(2):
            new_cand = Candidate(name=self.fake.first_name(), lastName=self.fake.last_name(), 
                idType=self.fake.country_code(), identification=self.fake.random_int(10999999, 99999999), 
                email=self.fake.email(), phone=self.fake.random_int(3001234567, 3109999999), country=self.fake.country(), 
                city=self.fake.city(), address=self.fake.street_address(), profession=self.fake.job(), 
                username=self.fake.user_name()
            )
            for y in range(2):
                new_cand.softSkills.append(SoftSkills(skill=self.fake.job(), candidate_id=new_cand.id))
            for y in range(2):
                new_cand.technicalSkills.append(TechnicalSkills(skill=self.fake.job(), candidate_id=new_cand.id))                

            db.session.add(new_cand)
            db.session.commit()
            cand_created = Candidate.query.filter(Candidate.name == new_cand.name).filter(Candidate.username==new_cand.username).order_by(Candidate.createdAt.desc()).first()
            self.candidateId = cand_created.id

        self.endpoint_get = '/candidates-qry?page=1&perPage=1'
        self.endpoint_health = '/candidates-qry/ping'
        self.content_type = 'application/json'

        self.endpoint_get_412 = '/candidates-qry/candidateId'
        self.endpoint_get_404 = '/candidates-qry/{}'.format(str(self.candidateId * 1000))
        self.endpoint_get_200 = '/candidates-qry/{}'.format(str(self.candidateId))


    def test_health(self):
        """Test for health check ping"""
        req_health = self.client.get(self.endpoint_health, headers={'Content-Type': self.content_type})
        json.loads(req_health.get_data())
        self.assertEqual(req_health.status_code, 200)

    def test_get_all_candidates_200(self):
        """Test get all candidates"""
        resp_get = self.client.get(self.endpoint_get, headers={'Content-Type': self.content_type})
        print(resp_get.get_data())
        self.assertEqual(resp_get.status_code, 200)

    def test_get_candidates_filter_200(self):
        """Test get candidates by filter"""
        resp_get = self.client.get(self.endpoint_get+"&technicalskill=Java&softskill=Comunicacion", headers={'Content-Type': self.content_type})
        print(resp_get.get_data())
        self.assertEqual(resp_get.status_code, 200)

    def test_get_candidate_404(self):
        #print("endpint404: ", self.endpoint_get_404)
        req_get = self.client.get(self.endpoint_get_404, headers={'Content-Type': self.content_type})
        #print(json.loads(req_get.get_data()))
        self.assertEqual(req_get.status_code, 404)

    def test_get_candidate_412(self):
        #print("endpint412: ", self.endpoint_get_412)
        req_get = self.client.get(self.endpoint_get_412, headers={'Content-Type': self.content_type})
        #print(json.loads(req_get.get_data()))
        self.assertEqual(req_get.status_code, 412)

    def test_get_candidate_200(self):
        req_get = self.client.get(self.endpoint_get_200, headers={'Content-Type': self.content_type})
        resp_get = json.loads(req_get.get_data())
        print(self.candidateId, resp_get["id"], resp_get["name"], resp_get["username"], resp_get["createdAt"])
        self.assertEqual(self.candidateId, resp_get["id"])
        self.assertEqual(req_get.status_code, 200)
