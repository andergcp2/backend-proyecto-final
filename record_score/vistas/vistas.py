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
    
class VistaRecordScore(Resource):

    def get(self, idcandidatetest):
        #Insertar codigo para validar token... solo debería consultar un usuario previamente registrado.
        return candidatetest_schema.dump(CandidateTest.query.get_or_404(idcandidatetest))
    
    def put(self, idcandidatetest):
        #Validar acceso con token
        data = request.get_json()
        required_fields = ["record"]
        if not all(field in data for field in required_fields):
            return customError(400, "CO01", f'Hay campos sin diligenciar. Campos requeridos: {required_fields}')
        
        pruebacandidato = CandidateTest.query.get_or_404(idcandidatetest)
        pruebacandidato.presentationdate = dt.datetime.now()
        pruebacandidato.qualificationtest = data["record"]
        pruebacandidato.testestatus = "FINALIZADA"
        db.session.commit()
        return candidatetest_schema.dump(pruebacandidato)
