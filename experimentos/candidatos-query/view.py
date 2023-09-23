import requests
from flask import request, current_app
from flask_restful import Resource
from model import db, Candidate, TestCandidate, CandidateSchema, TestCandidateSchema
from datetime import datetime

candidate_schema = CandidateSchema()
candidate_test_schema = TestCandidateSchema()


class HealthCheck(Resource):
    def get(self):
        return "ok"

class GetCandidate(Resource):

    def get(self, id):
        # resp = validate_token(request.headers)
        # if(resp['status_code'] != 200):
        #     return resp['msg'], resp['status_code']

        if id is not None: 
            try:
                int(id)
            except ValueError:
                return "id is not a number: {}".format(id), 400

        #print("GetCandidate-id: ", id)
        candidate = Candidate.query.filter(Candidate.id == id).first()
        if candidate is None:
            return "candidate does not exist", 404

        #return {"id": candidate.id, "firstname": candidate.firstname, "lastname": candidate.lastname, "createdAt": candidate.createdAt.isoformat()}, 200
        return candidate_schema.dump(candidate)


class GetTestsCandidate(Resource):

    def get(self, id):
        if id is not None: 
            try:
                int(id)
            except ValueError:
                return "id is not a number: {}".format(id), 400

        #print("GetTestsCandidate-id: ", id)
        candidate = Candidate.query.filter(Candidate.id == id).first()
        if candidate is None:
            return "candidate does not exist", 404

        pruebas = db.session.query(TestCandidate).select_from(TestCandidate).filter(TestCandidate.id_candidate==id).filter(TestCandidate.presented==False).all()
        return [candidate_test_schema.dump(test) for test in pruebas]
