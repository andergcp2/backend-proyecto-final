import requests
from flask import request, current_app
from flask_restful import Resource
from model import db, Prueba, PruebaSchema
from datetime import datetime

prueba_schema = PruebaSchema()



class HealthCheck(Resource):
    def get(self):
        return "ok"

class GetPrueba(Resource):

    def get(self, id):
        # resp = validate_token(request.headers)
        # if(resp['status_code'] != 200):
        #     return resp['msg'], resp['status_code']

        if id is not None: 
            try:
                int(id)
            except ValueError:
                return "id is not a number: {}".format(id), 400

        prueba = Prueba.query.filter(Prueba.id == id).first()
        if prueba is None:
            return "prueba does not exist", 404

        return {"id": prueba.id, "name": prueba.name, "createdAt": candidate.createdAt.isoformat()}, 200

