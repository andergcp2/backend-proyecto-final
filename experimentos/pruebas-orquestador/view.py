import json
import requests
from flask import request, current_app
from flask_restful import Resource

# def validateToken(headers):
#     try:
#         if 'Authorization' not in headers:
#             return {'msg': 'token is not in header', 'status_code': 400}
#         resp = requests.get(current_app.config['USERS'], headers = headers)
#         if (resp.status_code==200):
#             return {'msg': resp.json(), 'status_code': 200}
#         return {'msg': 'token not validated', 'status_code': resp.status_code} # resp.reason
#     except Exception as ex:
#         return {'msg': 'users connection failed {} -> {}'.format(current_app.config['USERS'], ex), 'status_code': 500}

def getPruebasCandidato(endpoint, headers):
    return get(endpoint, headers)

def getPrueba(endpoint, headers):
    return get(endpoint, headers)

def getPreguntasPrueba(endpoint, data, headers):
    return get(endpoint, data, headers)

def get(endpoint, headers):
    try:
        resp = requests.get(endpoint, headers = headers)
        if (resp.status_code==200):
            return {'msg': resp.json(), 'status_code': resp.status_code}
        return {'msg': resp.content, 'status_code': resp.status_code} 
    except Exception as ex:
        return {'msg': 'connection endpoint failed {} -> {}'.format(endpoint, ex), 'status_code': 500}

def create(endpoint, data, headers):
    try:
        resp = requests.post(endpoint, data=json.dumps(data), headers = headers)
        if (resp.status_code==201):
            return {'msg': resp.json(), 'status_code': resp.status_code} 
        return {'msg': resp.content, 'status_code': resp.status_code} 
    except Exception as ex:
        return {'msg': 'connection endpoint failed {} -> {}'.format(endpoint, ex), 'status_code': 500}
    
class HealthCheck(Resource):
    def get(self):
        return "ok"

class PruebaInit(Resource):

    def post(self, candidatoId, pruebaId):
        # 400 - En el caso que alguno de los campos no esté presente en la solicitud
        if candidatoId is None or pruebaId is None: 
            return "parameter(s) missing", 400

        # 401 - El token no es válido o está vencido.
        # headers = {"Content-Type":"application/json", "Authorization": request.headers['Authorization']}
        # resp = validateToken(headers)
        # status_code = resp['status_code']
        # if(status_code != 200):
        #     return resp['msg'], status_code
        # userId = resp["msg"]["id"]

        # 404 - El candidato que va iniciar la prueba no existe
        endpointC = format(current_app.config['CANDIDATOS_QUERY']) +"/{}".format(candidatoId)
        resp = getPrueba(endpointC, headers)
        #print ("candidato: ", endpointC, resp)
        status_code = resp['status_code']
        if(status_code != 200):
            return resp['msg'], status_code

        # 404 - La prueba que se quiere iniciar no existe
        endpointT = format(current_app.config['PRUEBAS_QUERY']) +"/{}".format(pruebaId)
        resp = getPrueba(endpointT, headers)
        #print ("prueba: ", endpointT, resp)
        status_code = resp['status_code']
        if(status_code != 200):
            return resp['msg'], status_code

        endpointQ = format(current_app.config['PREGUNTAS_QUERY']) +"/{}".format(pruebaId)
        resp = getPreguntasPrueba(endpointQ, headers)
        #print ("preguntas: ", endpointQ, resp)
        status_code = resp['status_code']
        if(status_code != 200):
            return resp['msg'], status_code

        # en este punto se almacenan el subconjunto de preguntas y respuestas de la prueba 
        # que está presentando el candidato utilizando como llave los ids candidatoId-pruebaId
        # ...
        # se extrae la primera pregunta y sus respuestas para iniciar la prueba

        data = {
            "pruebaId": pruebaId,
            "candidatoId": candidatoId,
            "question": resp['question'],
            "answers": resp['answers']
        }

        #return json.dumps(data), 201
        return data, 201


class PruebaNext(Resource):

    def post(self, candidatoId, pruebaId):
        # 400 - En el caso que alguno de los campos no esté presente en la solicitud
        if candidatoId is None or pruebaId is None: 
            return "parameter(s) missing", 400

        # en este punto se consulta de cache la siguiente pregunta y sus respectivas respuestas 
        # de la prueba que está presentando el candidato utilizando los ids candidatoId-pruebaId
        # ...

        data = {
            "pruebaId": pruebaId,
            "candidatoId": candidatoId,
            "question": resp['question'],
            "answers": resp['answers']
        }
        return data, 201


class PruebaDone(Resource):

    def post(self, candidatoId, pruebaId):
        # 400 - En el caso que alguno de los campos no esté presente en la solicitud
        if candidatoId is None or pruebaId is None: 
            return "parameter(s) missing", 400

        # en este punto se calcula el resultado de la prueba que está presentando el candidato 
        # consultando de cache las preguntas, sus respuestas y las respuestas del candidato
        # ...
        result = 0

        data = {
            "pruebaId": pruebaId,
            "candidatoId": candidatoId,
            "result": result
        }
        return data, 201