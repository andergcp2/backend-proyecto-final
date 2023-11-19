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
        #Insertar codigo para validar token... solo debería consultar un usuario previamente registrado.
        role = request.args.getlist('role')
        typet = request.args.getlist('typet')
        fini = request.args.getlist('fini')
        ffin = request.args.getlist('ffin')
        idcandidate = request.args.getlist('idcandidate')
        page = request.args.get('page')
        per_page = request.args.get('perPage')
      
        if not role and not page and not per_page and not typet and not fini and not ffin and not idcandidate:
            return [interviewcandidate_schema.dump(interviewcandidate) for interviewcandidate in InterviewCandidate.query.all()]
        elif not role and not type:
            result = InterviewCandidate.query.paginate(page=int(page), per_page=int(per_page))
            response = {
                    'items': [interviewcandidate_schema.dump(interviewcandidate) for interviewcandidate in result],
                    'page': page,
                    'total_items': result.total,
                    'pages': result.pages
                }
            return response, 200
        
        my_filters = set()
        buscart=0
        buscarf=0
        
        if typet:
            if typet == 0:
                lista = ["FINALIZADA", "CANCELADA"]
                buscart = 1
            else:
                lista = ["ASIGNADA", "PROGRAMADA"]
                buscart = 2
            my_filters.add(InterviewCandidate.interviewstatus.in_(lista))
        
        if fini and ffin and validarFechaISO(fini[0]) and validarFechaISO(ffin[0]):
            fini = datetime.fromisoformat(fini[0])
            ffin = datetime.fromisoformat(ffin[0])
            buscarf=1
        elif fini and not ffin and validarFechaISO(fini[0]):
            fini = datetime.fromisoformat(fini[0])
            ffin = dt.date.today()
            buscarf=1
        elif not fini and ffin:
            return customError(400, "CO01", f'No es posible consultar un rando sin fecha de inicio')
        elif not validarFechaISO(fini) and not validarFechaISO(ffin):
            return customError(400, "CO03", f'Los formatos de fecha no corresponden')
        
        if buscarf:
            
            if buscart == 1:
                my_filters.add(InterviewCandidate.presentationdate>=fini)
                my_filters.add(InterviewCandidate.presentationdate<=ffin)
            if buscart == 2:
                my_filters.add(InterviewCandidate.summonsdate>=fini)
                my_filters.add(InterviewCandidate.summonsdate<=ffin)

        if idcandidate:
            idcandidate = idcandidate[0]
            my_filters.add(InterviewCandidate.idcandidate==idcandidate)

        if not page and not per_page:
            page = 1
            per_page = 10

        result = InterviewCandidate.query.filter(*my_filters).paginate(page=int(page), per_page=int(per_page))

        response = {
                    'items': [interviewcandidate_schema.dump(interviewcandidate) for interviewcandidate in result],
                    'page': page,
                    'total_items': result.total,
                    'pages': result.pages
                }
        return response, 200
    
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

    def put(self, idcandidateinterview):
        data = request.get_json()
        required_fields = ["presentationdate","qualificationtest"]
        if not all(field in data for field in required_fields):
            return customError(400, "CO01", f'Hay campos sin diligenciar. Campos requeridos: {required_fields}')
        
        pruebacandidato = InterviewCandidate.query.get_or_404(idcandidateinterview)
        pruebacandidato.presentationdate = dt.datetime.now()
        pruebacandidato.qualificationtest = data["qualificationtest"]
        pruebacandidato.testestatus = "FINALIZADA"
        db.session.commit()
        return interviewcandidate_schema.dump(pruebacandidato)
      
class VistaTestsAssignedToCandidates(Resource):
    
    def get(self,idcandidate):
        lista = ["FINALIZADA", "CANCELADA"]
        candidatest = [interviewcandidate_schema.dump(candidatetest) for candidatetest in InterviewCandidate.query.filter(InterviewCandidate.idcandidate==idcandidate).filter(InterviewCandidate.testestatus.not_in(lista)).all()]
        
        for candidatet in candidatest:
            print(candidatet)
            response = requests.get("{0}/{1}".format(current_app.config['TEST_QRY_URL'], candidatet["idtest"]), headers={"Content-Type":"application/json"}, timeout=60)
            candidatet["test"]=json.loads(response.text)
        
        return candidatest, 200
    