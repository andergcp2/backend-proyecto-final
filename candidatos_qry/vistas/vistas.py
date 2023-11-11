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
        page = request.args.get('Page')
        per_page = request.args.get('Per-page')

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

        if role is not None:
            my_filters.add(Candidate.profession.in_(role))
        if softskill is not None:
            my_filters.add(SoftSkills.skill.in_(softskill))
        if technicalskill is not None:
            my_filters.add(TechnicalSkills.skill.in_(technicalskill))


        result = Candidate.query.join(SoftSkills).join(TechnicalSkills).filter(*my_filters).paginate(page=int(page), per_page=int(per_page))
        
        response = {
                'items': [candidate_schema.dump(candidate) for candidate in result],
                'page': page,
                'total_items': result.total,
                'pages': result.pages
            }
        if result.total != 0:
            return response, 200
        else:
            return response, 404

        