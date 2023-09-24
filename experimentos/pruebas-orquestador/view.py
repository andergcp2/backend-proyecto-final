import json
import requests
from flask import request, current_app
from flask_restful import Resource

def getPruebasCandidato(endpoint, headers):
    return get(endpoint, headers)

def getCandidato(endpoint, headers):
    return get(endpoint, headers)

def getPrueba(endpoint, headers):
    return get(endpoint, headers)

def getPreguntasPrueba(endpoint, data, headers):
    return get(endpoint, data, headers)

def updatePrueba(endpoint, data, headers):
    return update(endpoint, data, headers)

def get(endpoint, headers):
    try:
        resp = requests.get(endpoint, headers = headers)
        return resp
        # if (resp.status_code==200):
        #     return {'msg': resp.json(), 'status_code': resp.status_code}
        # return {'msg': resp.content, 'status_code': resp.status_code} 
    except Exception as ex:
        return {'msg': 'connection endpoint failed {} -> {}'.format(endpoint, ex), 'status_code': 500}
        # return (resp.text, resp.status_code, resp.headers.items())
        # return (ex, 500)

def update(endpoint, data, headers):
    try:
        resp = requests.post(endpoint, data=json.dumps(data), headers = headers)
        return resp
        # if (resp.status_code==201):
        #     return {'msg': resp.json(), 'status_code': resp.status_code} 
        # return {'msg': resp.text, 'status_code': resp.status_code} 
    except Exception as ex:
        return {'msg': 'connection endpoint failed {} -> {}'.format(endpoint, ex), 'status_code': 500}
    
class HealthCheck(Resource):
    def get(self):
        return "ok"

class PruebaInit(Resource):

    def post(self, candidatoId, pruebaId):
        headers = {"Content-Type":"application/json", "Authorization": request.headers['Authorization']}
        #print(current_app.config['CANDIDATOS_QUERY'])

        # 400 - En el caso que alguno de los campos no esté presente en la solicitud
        if candidatoId is None or pruebaId is None: 
            return "parameter(s) missing", 400

        # 404 - El candidato que va iniciar la prueba no existe
        endpointC = format(current_app.config['CANDIDATOS_QUERY']) +"/{}".format(candidatoId)
        resp = getCandidato(endpointC, headers)
        print ("candidato: ", endpointC, resp)
        
        #status_code = resp['status_code']
        if(resp.status_code != 200):
            print(resp.json())
            print('########################')
            return resp
            #return resp['msg'], status_code
            #return 'msg-test', status_code

        print('test no existe *****************************')

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

        # y se actualiza el resultado de la prueba para el candidato
        endpointP = format(current_app.config['CANDIDATOS_QUERY'])
        resp = updatePrueba(endpointP, data, headers)
        # print("prueba: ", endpointP, resp)
        status_code = resp['status_code']
        if(status_code != 201):
            return resp['msg'], status_code

        return data, 201