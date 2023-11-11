import json
from modelos import db, CandidateTest, CandidateTestSchema
from flask import request, current_app
from flask_restful import Resource
from .errors import customError
from .utils import lengthValidation
import requests
import datetime as dt
from datetime import timedelta

candidatetest_schema = CandidateTestSchema()

def validarEntero(numero):
    try:
        temp = int(numero)
        return True
    except ValueError:
        return False

class VistaPing(Resource):
    def get(self):
        return "PONG", 200
    
class VistaCandidateTest(Resource):

    def get(self):
        #Insertar codigo para validar token... solo debería consultar un usuario previamente registrado.
        return [candidatetest_schema.dump(candidatetest) for candidatetest in CandidateTest.query.all()]
    
    def post(self):
        data = request.get_json()
        required_fields = ["idcandidate", "idtest"]
        if not all(field in data for field in required_fields):
            return customError(400, "CO01", f'Hay campos sin diligenciar. Campos requeridos: {required_fields}')
        
        if validarEntero(data['idcandidate'])==False or validarEntero(data['idtest'])==False:
            return customError(400, "CO03", f'Los datos ingresados no cumplen el estandar de información')
        
        #Invocar para validar la existencia del candidato
        #Invocar para validar la existencia de la prueba
        #Traer el usuario que generó la creación del registro

        idcandidate = data['idcandidate']
        idtest = data['idtest']
        maxdatepresent = dt.date.today()+timedelta(days=10)
        testestatus = "ASIGNADA"

        lista = ["ASIGNADA","EN CURSO"]
        candidateQuery = CandidateTest.query.filter(CandidateTest.idcandidate==idcandidate,
                                                    CandidateTest.idtest==idtest,
                                                    CandidateTest.testestatus.in_(lista)).first()
        db.session.commit()
        if candidateQuery is None:
            new_candidatetest = CandidateTest(
                                    idcandidate = idcandidate,
                                    idtest = idtest,
                                    maxdatepresent = maxdatepresent,
                                    testestatus = testestatus
                                    )
            db.session.add(new_candidatetest)
            db.session.commit()
            return candidatetest_schema.dump(new_candidatetest), 201
        else:
            return customError(400, "CO05", f'La prueba seleccionada ya se encuentra asignada al candidato')
    
class VistaCandidateTestQry(Resource):

    def get(self,idcandidate):
        #Consultar con el token
        lista = ["FINALIZADA", "CANCELADA"]
        return [candidatetest_schema.dump(candidatetest) for candidatetest in CandidateTest.query.filter(CandidateTest.idcandidate==idcandidate).filter(CandidateTest.testestatus.not_in(lista)).all()],200
    
    def get(self,idtest, state):
        lista = ["FINALIZADA", "CANCELADA"]
        if state == 1:
            return [candidatetest_schema.dump(candidatetest) for candidatetest in CandidateTest.query.filter(CandidateTest.idtest==idtest).filter(CandidateTest.testestatus.not_in(lista)).all()],200
        else:
            return [candidatetest_schema.dump(candidatetest) for candidatetest in CandidateTest.query.filter(CandidateTest.idtest==idtest).filter(CandidateTest.testestatus.in_(lista)).all()],200