import requests
from flask import request
from flask_restful import Resource
from datetime import datetime
from .errors import customError
from .utils import lengthValidation

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
        required_fields = ["idType", "idNumber", "companyName", "industry", "email", "phone", "address", "country", "city", "reprName", "reprIdType", "reprIdNumber"]
        if not all(field in data for field in required_fields):
            return customError(400, "CO01", f'Hay campos sin diligenciar. Campos requeridos: {required_fields}')
        
        field_lengths = {
            "idType": (2, 4),
            "companyName": (3, 50),
            "industry": (3, 50),
            "email": (3, 100),
            "address": (3, 100),
            "country": (3, 50),
            "city": (3, 50),
            "reprName": (3, 100),
            "reprIdType": (2, 4),
        }
        
        for field, (min_len, max_len) in field_lengths.items():
            if not lengthValidation(data.get(field, ""), min_len, max_len):
                return customError(400, "CO02", f"El campo '{field}' no cumple con la longitud requerida: {min_len}-{max_len}")
        
        idType = data['idType']
        idNumber = data['idNumber']  
        companyName = data['companyName']
        industry = data['industry']
        email = data['email']
        phone = data['phone']
        address = data['address']
        country = data['country']
        city = data['city']
        reprName = data['reprName']
        reprIdType = data['reprIdType']
        reprIdNumber = data['reprIdNumber']
        #pendiente validaciones no crear empresa repetida
       
        new_company = Company(
                                idType=idType,
                                idNumber=idNumber,
                                companyName=companyName,
                                industry=industry,
                                email=email,
                                phone=phone,
                                address=address,
                                country=country,
                                city=city,
                                reprName=reprName,
                                reprIdType=reprIdType,
                                reprIdNumber=reprIdNumber
                                )
        db.session.add(new_company)
        db.session.commit()
        return company_schema.dump(new_company), 201