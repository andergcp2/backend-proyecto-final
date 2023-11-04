import json
from modelos import db, SoftSkills, TechnicalSkills, Candidate, CandidateSchema
from flask import request, current_app
from flask_restful import Resource
from .errors import customError
from .utils import lengthValidation
import requests

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
        

        if data['password'] != data['passwordConfirmation']:
            return customError(400, "CO03", "El campo password y passwordConfirmation no conciden")
        

        request_auth = {
            'username': data['username'],
            'password': data['password'],
            'email': data['email']
        }
        response = requests.post(current_app.config['USERS'], headers={"Content-Type":"application/json"}, json=request_auth, timeout=60)
        print(response)
        data_resp = json.loads(response.text)
        if data_resp.get('errorMessage') is not None:
            return customError(400, "CO04", f"Error en el registro del usuario en cognito - {data_resp.get('errorMessage')}")

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