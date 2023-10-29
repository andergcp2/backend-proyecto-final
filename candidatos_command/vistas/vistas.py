from modelos import db, SoftSkills, TechnicalSkills, Candidate, CandidateSchema
import requests
from flask import request
from flask_restful import Resource
from datetime import datetime
from .errors import customError
from .utils import lengthValidation

candidate_schema = CandidateSchema()

class VistaPing(Resource):
    def get(self):
        return "PONG", 200
    
class VistaCandidate(Resource):

    def get(self):
        #Validar si requiere token
        return [candidate_schema.dump(candidate) for candidate in Candidate.query.all()]
    
    def post(self):
        data = request.get_json()
        required_fields = ["name", "lastName", "idType", "identification", "email", "phone", "address", "country", "city", "profession", "username", "password", "passwordConfirmation"]
        if not all(field in data for field in required_fields):
            return customError(400, "CO01", f'Hay campos sin diligenciar. Campos requeridos: {required_fields}')
        
        field_lengths = {
            "idType": (2, 4),
            "name": (3, 50),
            "lastName": (3, 50),
            "email": (3, 100),
            "address": (3, 100),
            "country": (3, 50),
            "city": (3, 50),
            "profession": (3, 200),
            "username": (2, 50),
            "password": (6, 50)
        }
        
        for field, (min_len, max_len) in field_lengths.items():
            if not lengthValidation(data.get(field, ""), min_len, max_len):
                return customError(400, "CO02", f"El campo '{field}' no cumple con la longitud requerida: {min_len}-{max_len}")
        

        name = data['name']
        lastName = data['lastName']
        idType = data['idType']
        identification = data['identification']
        email = data['email']
        phone = data['phone']
        country = data['country']
        city = data['city']
        address = data['address']
        profession = data['profession']
        softSkillsArray = data['softSkills']
        technicalSkillsArray = data['technicalSkills']
        username = data['username']

        softSkills = []
        for softSkill in softSkillsArray:
            print(softSkill)
            new_skill = SoftSkills(skill = softSkill)
            softSkills.append(new_skill)

        technicalSkills = []
        for technicalSkill in technicalSkillsArray:
            print(technicalSkill)
            new_technical_skill = TechnicalSkills(skill = technicalSkill)
            technicalSkills.append(new_technical_skill)

        #pendiente validaciones no crear empresa repetida
       
        new_candidate = Candidate(
                                name = name,
                                lastName = lastName,
                                idType = idType,
                                identification = identification,
                                email = email,
                                phone = phone,
                                country = country,
                                city = city,
                                address = address,
                                profession = profession,
                                softSkills = softSkills,
                                technicalSkills = technicalSkills,
                                username = username
                                )
        db.session.add(new_candidate)
        db.session.commit()
        return candidate_schema.dump(new_candidate), 201