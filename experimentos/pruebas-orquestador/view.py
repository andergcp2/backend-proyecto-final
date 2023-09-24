import json, requests
from flask import request, Response, current_app
from flask_restful import Resource

def getPruebasCandidato(endpoint, headers):
    return get(endpoint, headers)

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
        resp = get(endpointC, headers)
        print ("candidato: ", endpointC, resp)

        # if(resp.status_code != 200):
        #     return Response(resp.json(), resp.status_code, resp.headers.items())

        # 404 - La prueba que se quiere iniciar no existe
        endpointT = format(current_app.config['PRUEBAS_QUERY']) +"/{}".format(pruebaId)
        resp = get(endpointT, headers)
        print ("prueba: ", endpointT, resp)

        # if(resp.status_code != 200):
        #     return Response(resp.json(), resp.status_code, resp.headers.items())

        endpointQ = format(current_app.config['PREGUNTAS_QUERY']) +"/{}".format(pruebaId)
        resp = get(endpointQ, headers)
        print ("preguntas: ", endpointQ, resp)
        
        if(resp.status_code != 200):
            return Response(resp.json(), resp.status_code, resp.headers.items())

        print ("####################################")

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