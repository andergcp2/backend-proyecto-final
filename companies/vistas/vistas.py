import requests
from flask import request, current_app
from flask_restful import Resource
from datetime import datetime

from modelos import db, Company, CompanySchema

company_schema = CompanySchema()

class VistaPing(Resource):
    def get(self):
        return "PONG", 200
    
class VistaCompany(Resource):

    def get(self):
        #Validar si requiere token
        return [company_schema.dump(company) for company in Company.query.all()]
    
    def post(self):
        data = request.get_json()
        if "tipoIde" not in data or "numeroIde" not in data or "razonsocial" not in data or "sector" not in data or "correo" not in data or "telefono" not in data or "direccion" not in data:
            return "Campos obligatorios sin diligenciar", 400
        tipoIde = request.json['tipoIde']
        numeroIde = request.json['numeroIde']
        razonsocial = request.json['razonsocial']
        sector = request.json['sector']
        correo = request.json['correo']
        telefono = request.json['telefono']
        direccion = request.json['direccion']
        #pendiente validaciones
        nuevo_company = Company(tipoIde=tipoIde,
                                numeroIde=numeroIde,
                                razonsocial=razonsocial,
                                sector=sector,
                                correo=correo,
                                telefono=telefono,
                                direccion=direccion)
        db.session.add(nuevo_company)
        db.session.commit()
        return company_schema.dump(nuevo_company), 201