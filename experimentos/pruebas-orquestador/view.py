import json, requests, redis
from flask import request, Response, current_app
from flask_restful import Resource
#from redis_client import RedisClient

def getPruebasCandidato(endpoint, headers):
    return get(endpoint, headers)

def get(endpoint, headers):
    try:
        resp = requests.get(endpoint, headers = headers)
        return resp
    except Exception as ex:
        return {'msg': 'connection endpoint failed {} -> {}'.format(endpoint, ex), 'status_code': 500}
        # return (resp.json, resp.status_code, resp.headers.items())

def update(endpoint, data, headers):
    try:
        resp = requests.post(endpoint, data=json.dumps(data), headers = headers)
        return resp
    except Exception as ex:
        return {'msg': 'connection endpoint failed {} -> {}'.format(endpoint, ex), 'status_code': 500}
        #return (resp.json, resp.status_code, resp.headers.items())

class HealthCheck(Resource):
    def get(self):
        return "ok"

class PruebaInit(Resource):
    def __init__(self) -> None:
        pool = redis.ConnectionPool(host=current_app.config['ELASTICACHE_HOST'], port=current_app.config['ELASTICACHE_PORT'], db=0)
        self.redis = redis.Redis(connection_pool=pool)
        #self.publisher = pubsub_v1.PublisherClient()
        #self.topic_path = self.publisher.topic_path(current_app.config['PROJECT'], current_app.config['TOPIC'])
        # self.redis_cli = redis.Redis(host="10.182.0.3", port=6379, decode_responses=True, encoding="utf-8", )
        super().__init__()

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

        print("\n--------------------------")
        #RedisClient.redis_ping()
        self.redis.set('mykey', 'redis-abc-jobs')
        print(self.redis.get('mykey'))
        print("--------------------------\n")

        # return json.dumps({'test':'ok'}), 200

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
        return data, 200


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