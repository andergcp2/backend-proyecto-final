import datetime
import json
from modelos import db, InterviewCandidate, InterviewCandidateSchema
from flask import request, current_app
from flask_restful import Resource
from .errors import customError
from .utils import lengthValidation
import requests
import datetime as dt
from datetime import datetime

interviewcandidate_schema = InterviewCandidateSchema()

def validarEntero(numero):
    try:
        temp = int(numero)
        return True
    except ValueError:
        return False

def validarFechaISO(fecha):
    try:
        fecha = datetime.fromisoformat(fecha)
        return True
    except ValueError:
        return False

class VistaPing(Resource):
    def get(self):
        return "PONG", 200
    
class VistaCandidateInterview(Resource):

    def get(self):
        return [interviewcandidate_schema.dump(interviewcandidate) for interviewcandidate in InterviewCandidate.query.all()]

    def post(self):
        data = request.get_json()
        required_fields = ["candidateId", "companyId","projectId","interviewDate"]
        if not all(field in data for field in required_fields):
            return customError(400, "CO01", f'Hay campos sin diligenciar. Campos requeridos: {required_fields}')
        
        if validarEntero(data['candidateId']) == False or validarEntero(data['companyId'])==False or validarEntero(data['projectId'])==False or validarFechaISO(data['interviewDate'])==False:
            return customError(400, "CO03", f'Los datos ingresados no cumplen el estandar de información')
        
        if validarFechaISO(data['interviewDate']):
            interviewDate = datetime.fromisoformat(data['interviewDate'])
            
        actual = datetime.now()
        if interviewDate < actual:
            return customError(400, "CO06", f'La fecha no puede ser inferior a la fecha actual')
        
        candidateId = data['candidateId']
        companyId = data['companyId']
        projectId = data['projectId']
        status = "CREADA"

        candidateQuery = InterviewCandidate.query.filter(InterviewCandidate.candidateId==candidateId,
                                                        InterviewCandidate.companyId==companyId,
                                                        InterviewCandidate.projectId==projectId,
                                                        InterviewCandidate.status==status).first()
        db.session.commit()
        if candidateQuery is None:
            new_candidateinterview = InterviewCandidate(
                                            candidateId = candidateId,
                                            companyId = companyId,
                                            projectId = projectId,
                                            interviewDate = interviewDate,
                                            status = status
                                        )
            db.session.add(new_candidateinterview)
            db.session.commit()
            return interviewcandidate_schema.dump(new_candidateinterview), 201
        else:
            return customError(400, "CO05", f'La entrevista seleccionada ya se encuentra asignada al candidato')
    

      
class VistaTestsAssignedToCandidates(Resource):
    
    def get(self,candidateId):
        candidatest = [interviewcandidate_schema.dump(candidatetest) for candidatetest in InterviewCandidate.query.filter(InterviewCandidate.candidateId==candidateId).all()]
        
        for candidatet in candidatest:
            print(candidatet)
            response = requests.get("{0}/{1}".format(current_app.config['TEST_QRY_URL'], candidatet["idtest"]), headers={"Content-Type":"application/json"}, timeout=60)
            candidatet["test"]=json.loads(response.text)
        
        return candidatest, 200
    
class VistaUpdateInterviewCandidate(Resource):
    def put(self, interviewId):
        data = request.get_json()
        required_fields = ["score"]
        if not all(field in data for field in required_fields):
            return customError(400, "CO01", f'Hay campos sin diligenciar. Campos requeridos: {required_fields}')
        
        pruebacandidato = InterviewCandidate.query.get_or_404(interviewId)
        pruebacandidato.score = data["score"]
        pruebacandidato.comment = data["comment"]
        pruebacandidato.status = "FINALIZADA"
        db.session.commit()
        return interviewcandidate_schema.dump(pruebacandidato)
    
class VistaCandidateInterviewSearch(Resource):

    def get(self, companyId, projectId):
        #Insertar codigo para validar token... solo debería consultar un usuario previamente registrado.
        bandera = 0
        role = request.args.getlist('role')
        status = request.args.getlist('status')
        fini = request.args.getlist('fini')
        print(fini)
        ffin = request.args.getlist('ffin')
        candidateId = request.args.getlist('candidateId')
        print(candidateId)
        page = request.args.get('page')
        per_page = request.args.get('perPage')
      
        if not page and not per_page:
            page = 1
            per_page = 20
        
        my_filters = set()
        
        my_filters.add(InterviewCandidate.companyId==companyId)
        my_filters.add(InterviewCandidate.projectId==projectId)

        if status:
            my_filters.add(InterviewCandidate.status==status)

        if fini:
            if validarFechaISO(fini[0]):
                fini=fini[0]
                fini = datetime.fromisoformat(fini)
                bandera = 1
        if ffin:
            if validarFechaISO(ffin[0]):
                ffin=ffin[0]
                ffin = datetime.fromisoformat(ffin)
                if bandera == 0:
                    return customError(400, "CO01", f'No es posible consultar un rando sin fecha de inicio') 
        
        if bandera==1 and not ffin:
            actual = datetime.today()
            if actual < fini:
                ffin = fini
            else:
                ffin = actual
        
        if fini and ffin:
            my_filters.add(InterviewCandidate.interviewDate.between(fini,ffin))

        if candidateId:
            candidateId = candidateId[0]
            my_filters.add(InterviewCandidate.candidateId==candidateId)

        result = InterviewCandidate.query.filter(*my_filters).paginate(page=int(page), per_page=int(per_page))

        response = {
                    'items': [interviewcandidate_schema.dump(interviewcandidate) for interviewcandidate in result],
                    'page': page,
                    'total_items': result.total,
                    'pages': result.pages
                }
        return response, 200
    
