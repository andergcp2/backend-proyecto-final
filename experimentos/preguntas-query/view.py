import json, requests
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
                data = {'error': 'id {} is not a number'.format(id)}
                return json.dumps(data), 400

        #print("GetPregunta-id: ", id)
        pregunta = Pregunta.query.filter(Pregunta.id == id).first()
        if pregunta is None:
            return "pregunta does not exist", 404
        return pregunta_schema.dump(pregunta)

class GetPreguntas(Resource):

    def get(self):
        preguntas = db.session.query(Pregunta).select_from(Pregunta).all()
        return [pregunta_schema.dump(p) for p in preguntas]

class GetRespuestasPregunta(Resource):

    def get(self, id):
        if id is not None: 
            try:
                int(id)
            except ValueError:
                data = {'error': 'id {} is not a number'.format(id)}
                return json.dumps(data), 400

        #print("GetRespuestasPregunta-id: ", id)
        pregunta = Pregunta.query.filter(Pregunta.id == id).first()
        if pregunta is None:
            data = {'error': 'pregunta {} does not exist'.format(id)}
            return json.dumps(data), 404

        respuestas = db.session.query(Respuesta).select_from(Respuesta).filter(Respuesta.preguntaId==id).all()
        return [respuesta_schema.dump(answer) for answer in respuestas]

class GetPreguntasRespuestasPrueba(Resource):

    def get(self, testId):
        if testId is not None: 
            try:
                int(testId)
            except ValueError:
                data = {'error': 'id {} is not a number'.format(testId)}
                return json.dumps(data), 400

        preguntas = db.session.query(Pregunta, Respuesta).filter(Pregunta.id==Respuesta.preguntaId).filter(Pregunta.pruebaId==testId).all()
        questions_answers = [{'question': pregunta_schema.dump(p[0]), 'answer': respuesta_schema.dump(p[1])} for p in preguntas]
        return json.dumps(questions_answers)
        # return [pregunta_schema.dump(p) for p in preguntas]
