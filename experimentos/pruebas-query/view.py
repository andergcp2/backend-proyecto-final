import requests
from flask import request, current_app
from flask_restful import Resource
from model import db, Prueba, PruebaSchema
from datetime import datetime

test_schema = PruebaSchema()

class HealthCheck(Resource):
    def get(self):
        return "ok"

class GetTest(Resource):

    def get(self, id):
        # resp = validate_token(request.headers)
        # if(resp['status_code'] != 200):
        #     return resp['msg'], resp['status_code']

        if id is not None: 
            try:
                int(id)
            except ValueError:
                return "id is not a number: {}".format(id), 400

        test = Prueba.query.filter(Prueba.id == id).first()
        if test is None:
            return "prueba does not exist", 404

        return test_schema.dump(test)


class GetTests(Resource):

    def get(self):
        tests = db.session.query(Prueba).select_from(Prueba).all()
        return [test_schema.dump(t) for t in tests]