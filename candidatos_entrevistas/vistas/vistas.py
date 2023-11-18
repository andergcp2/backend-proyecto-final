import json
from modelos import db, InterviewCandidate, InterviewCandidateSchema
from flask import request, current_app
from flask_restful import Resource
from .errors import customError
from .utils import lengthValidation
import requests
import datetime as dt
from datetime import timedelta

interviewcandidate_schema = InterviewCandidateSchema()

def validarEntero(numero):
    try:
        temp = int(numero)
        return True
    except ValueError:
        return False

class VistaPing(Resource):
    def get(self):
        return "PONG", 200
    
class VistaCandidateInterview(Resource):

    def get(self):
        #Insertar codigo para validar token... solo debería consultar un usuario previamente registrado.
        '''
        result = Candidate.query.join(SoftSkills).join(TechnicalSkills).filter(*my_filters).paginate(page=int(page), per_page=int(per_page))
        
        response = {
                'items': [candidate_schema.dump(candidate) for candidate in result],
                'page': page,
                'total_items': result.total,
                'pages': result.pages
            }

        return response, 200
        '''
        return [interviewcandidate_schema.dump(interviewcandidate) for interviewcandidate in InterviewCandidate.query.all()]
    
    def post(self):
        data = request.get_json()
        required_fields = ["idcandidate", "idinterview","summonsdate"]
        if not all(field in data for field in required_fields):
            return customError(400, "CO01", f'Hay campos sin diligenciar. Campos requeridos: {required_fields}')
        
        if validarEntero(data['idcandidate'])==False:
            return customError(400, "CO03", f'Los datos ingresados no cumplen el estandar de información')
        
        #Invocar para validar la existencia del candidato
        #Invocar para validar la existencia de la prueba
        #Traer el usuario que generó la creación del registro

        idcandidate = data['idcandidate']
        idinterview = data['idinterview']
        summonsdate = data['summonsdate']
        interviewstatus = "ASIGNADA"

        lista = ["ASIGNADA","EN CURSO"]
        candidateQuery = InterviewCandidate.query.filter(InterviewCandidate.idcandidate==idcandidate,
                                                    InterviewCandidate.idtest==idinterview,
                                                    InterviewCandidate.testestatus.in_(lista)).first()
        db.session.commit()
        if candidateQuery is None:
            new_candidateinterview = InterviewCandidate(
                                    idcandidate = idcandidate,
                                    idinterview = idinterview,
                                    summonsdate = summonsdate,
                                    interviewstatus = interviewstatus
                                    )
            db.session.add(new_candidateinterview)
            db.session.commit()
            return interviewcandidate_schema.dump(new_candidateinterview), 201
        else:
            return customError(400, "CO05", f'La entrevista seleccionada ya se encuentra asignada al candidato')
      
class VistaTestsAssignedToCandidates(Resource):
    
    def get(self,idcandidate):
        lista = ["FINALIZADA", "CANCELADA"]
        candidatest = [interviewcandidate_schema.dump(candidatetest) for candidatetest in InterviewCandidate.query.filter(InterviewCandidate.idcandidate==idcandidate).filter(InterviewCandidate.testestatus.not_in(lista)).all()]
        '''
        for candidatet in candidatest:
            print(candidatet)
            response = requests.get("{0}/{1}".format(current_app.config['TEST_QRY_URL'], candidatet["idtest"]), headers={"Content-Type":"application/json"}, timeout=60)
            candidatet["test"]=json.loads(response.text)
        '''
        return candidatest, 200
    