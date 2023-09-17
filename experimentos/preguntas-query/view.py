import requests
from flask import request, current_app
from flask_restful import Resource
from model import db, Pregunta, Respuesta, PreguntaSchema, RespuestaSchema
from datetime import datetime

pregunta_schema = PreguntaSchema()
respuesta_schema = PreguntaSchema()

class HealthCheck(Resource):
    def get(self):
        return "ok"

class GetPreguntas(Resource):

    def get(self, id):
        # resp = validate_token(request.headers)
        # if(resp['status_code'] != 200):
        #     return resp['msg'], resp['status_code']

        if id is not None: 
            try:
                int(id)
            except ValueError:
                return "id is not a number: {}".format(id), 400

        preguntas = db.session.query(Pregunta).select_from(Pregunta).join(Respuesta.preguntaId).filter(Pregunta.pruebaId==id).all()
        return [respuesta_schema.dump(q) for q in preguntas]
