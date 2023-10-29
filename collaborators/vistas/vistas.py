import requests
from flask import request
from flask_restful import Resource
from datetime import datetime
from .errors import customError
from .utils import lengthValidation

from modelos import db, Collaborator, CollaboratorSchema

collaborator_schema = CollaboratorSchema()

class VistaPing(Resource):
    def get(self):
        return "PONG", 200
    
class VistaCollaborators(Resource):

    def get(self):
        #Validar si requiere token
        return [collaborator_schema.dump(collaborator) for collaborator in Collaborator.query.all()]
    
    def post(self):
        data = request.get_json()
        required_fields = ["idType", "idNumber", "collaboratorName", "collaboratorLastName", "email", "phone", "address", "role", "position"]
        if not all(field in data for field in required_fields):
            return customError(400, "CO01", f'Hay campos sin diligenciar. Campos requeridos: {required_fields}')
        
        field_lengths = {
            "idType": (2, 4),
            "collaboratorName": (3, 50),
            "collaboratorLastName": (3, 50),
            "email": (3, 100),
            "address": (3, 100),
            "role": (3, 200),
            "position": (3, 200)
        }
        
        for field, (min_len, max_len) in field_lengths.items():
            if not lengthValidation(data.get(field, ""), min_len, max_len):
                return customError(400, "CO02", f"El campo '{field}' no cumple con la longitud requerida: {min_len}-{max_len}")
        
        idType = data['idType']
        idNumber = data['idNumber']  
        collaboratorName = data['collaboratorName']
        collaboratorLastName = data['collaboratorLastName']
        email = data['email']
        phone = data['phone']
        address = data['address']
        role = data['role']
        position = data['position']
        
        #pendiente validaciones no crear colaborador repetido
       
        new_collaborator = Collaborator(
                                idType=idType,
                                idNumber=idNumber,
                                collaboratorName=collaboratorName,
                                collaboratorLastName=collaboratorLastName,
                                email=email,
                                phone=phone,
                                address=address,
                                role=role,
                                position=position
                                )
        db.session.add(new_collaborator)
        db.session.commit()
        return collaborator_schema.dump(new_collaborator), 201