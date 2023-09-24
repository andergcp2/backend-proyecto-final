import requests
from flask import request, current_app
from flask_restful import Resource
from model import db, Pregunta, Respuesta, PreguntaSchema, RespuestaSchema
from datetime import datetime

pregunta_schema = PreguntaSchema()
respuesta_schema = RespuestaSchema()

class HealthCheck(Resource):
    def get(self):
        return "ok"

class GetPregunta(Resource):

    def get(self, id):
        if id is not None: 
            try:
                int(id)
            except ValueError:
                return "id is not a number: {}".format(id), 400

        #print("GetPregunta-id: ", id)
        pregunta = Pregunta.query.filter(Pregunta.id == id).first()
        if pregunta is None:
            return "pregunta does not exist", 404
        return pregunta_schema.dump(pregunta)


class GetRespuestasPregunta(Resource):

    def get(self, id):
        if id is not None: 
            try:
                int(id)
            except ValueError:
                return "id is not a number: {}".format(id), 400

        #print("GetRespuestasPregunta-id: ", id)
        pregunta = Pregunta.query.filter(Pregunta.id == id).first()
        if pregunta is None:
            return "pregunta does not exist", 404

        respuestas = db.session.query(Respuesta).select_from(Respuesta).filter(Respuesta.preguntaId==id).all()
        return [respuesta_schema.dump(answer) for answer in respuestas]
