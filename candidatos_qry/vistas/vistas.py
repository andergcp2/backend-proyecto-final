from modelos import SoftSkills, TechnicalSkills, Candidate, CandidateSchema
from flask import request
from flask_restful import Resource

candidate_schema = CandidateSchema()

class VistaPing(Resource):
    """ View for health """
    def get(self):
        """ Method ping return 200 """
        return "PONG", 200

class VistaSearch(Resource):
    """ View for search candidates by attributes """
    def get(self):
        """ Method get candidates by query params """
        role = request.args.get('role')
        softskill = request.args.get('softskill')
        technicalskill = request.args.get('technicalskill')

        if role is None and softskill is None and technicalskill is None:
            return [candidate_schema.dump(candidate) for candidate in Candidate.query.all()], 200

        my_filters = set()

        if role is not None:
            my_filters.add(Candidate.profession == role)
        if softskill is not None:
            my_filters.add(SoftSkills.skill == softskill)
        if technicalskill is not None:
            my_filters.add(TechnicalSkills.skill == technicalskill)

        candidates = [candidate_schema.dump(candidate) for candidate in Candidate.query.join(SoftSkills).join(TechnicalSkills).filter(*my_filters).all()]
        if candidates:
            return candidates, 200
        else:
            return candidates, 404
        