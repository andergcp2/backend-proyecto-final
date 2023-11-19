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
        role = request.args.getlist('role')
        softskill = request.args.getlist('softskill')
        technicalskill = request.args.getlist('technicalskill')
        page = request.args.get('page')
        per_page = request.args.get('perPage')

        if not role and not softskill and not technicalskill:
            result = Candidate.query.paginate(page=int(page), per_page=int(per_page))
            response = {
                'items': [candidate_schema.dump(candidate) for candidate in result],
                'page': page,
                'total_items': result.total,
                'pages': result.pages
            }
            return response, 200

        my_filters = set()

        if role:
            my_filters.add(Candidate.profession.in_(role))
        if softskill:
            my_filters.add(SoftSkills.skill.in_(softskill))
        if technicalskill:
            my_filters.add(TechnicalSkills.skill.in_(technicalskill))

        print(softskill)
        result = Candidate.query.join(SoftSkills).join(TechnicalSkills).filter(*my_filters).paginate(page=int(page), per_page=int(per_page))
        
        response = {
                'items': [candidate_schema.dump(candidate) for candidate in result],
                'page': page,
                'total_items': result.total,
                'pages': result.pages
            }

        return response, 200

class VistaGetCandidate(Resource):

    def get(self, id):
        if id is None: 
            return "candidate id is required", 400
        try:
            int(id)
        except ValueError:
            return "candidate id is not a number", 412

        candidate = Candidate.query.filter(Candidate.id == id).first()
        if candidate is None:
            return "candidate with the given id was not found", 404

        return candidate_schema.dump(candidate)
