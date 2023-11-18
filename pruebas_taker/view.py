import json, requests, redis
from flask import request, Response, current_app
from flask_restful import Resource
#from redis_client import RedisClient

def getPrueba(endpoint, headers):
    return get(endpoint, headers)

def getCandidato(endpoint, headers):
    return get(endpoint, headers)

def getPruebaCandidato(endpoint, headers):
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
        pool = redis.ConnectionPool(host=current_app.config['CACHE_HOST'], port=current_app.config['CACHE_PORT'], db=0)
        self.redis = redis.Redis(connection_pool=pool)
        # self.redis_cli = redis.Redis(host="10.182.0.3", port=6379, decode_responses=True, encoding="utf-8", )
        super().__init__()

    def post(self, candidatoId, pruebaId):
        headers = {"Content-Type":"application/json", "Authorization": request.headers['Authorization']}

        # 400 - En el caso que alguno de los campos no esté presente en la solicitud
        if candidatoId is None or pruebaId is None: 
            return "parameter(s) missing", 400

        print(current_app.config['CANDIDATOS_QUERY'])
        endpoint = format(current_app.config['CANDIDATOS_QUERY']) +"/{}".format(candidatoId)
        resp = getCandidato(endpoint, headers)
        print ("candidato-resp: ", endpoint, resp.json())

        # 404 - El candidato que va iniciar la prueba no existe
        if(resp.status_code != 200):
            return Response(resp.json(), resp.status_code, resp.headers.items())

        print(current_app.config['PRUEBAS_QUERY'])
        endpoint = format(current_app.config['PRUEBAS_QUERY']) +"/{}".format(pruebaId)
        resp = get(endpoint, headers)
        print ("prueba-resp: ", endpoint, resp.json())

        # 404 - La prueba a iniciar no existe
        if(resp.status_code != 200):
            return Response(resp.json(), resp.status_code, resp.headers.items())

        print(current_app.config['CANDIDATOS_PRUEBAS'])
        endpoint = format(current_app.config['CANDIDATOS_PRUEBAS']) +"/{}/{}".format(candidatoId, pruebaId)
        resp = get(endpoint, headers)
        print ("candidatos-pruebas-res: ", endpoint, resp.json())

        # 404 - El candidato que va iniciar la prueba no existe
        if(resp.status_code != 200):
            return Response(resp.json(), resp.status_code, resp.headers.items())

        mango = True
        data = {
            "pruebaId": pruebaId,
            "candidatoId": candidatoId
        }
        if (mango):
            return json.dumps(data), 200

        idcache = pruebaId+"-"+candidatoId
        #self.redis.delete(idcache)

        questionsTest = []
        questions = json.loads(resp.json())
        # se cargan 10 preguntas por default
        for x in range(0, 50, 5):
            y=x
            answers = []
            question = questions[x]['question']
            #print("")
            #print(x, question)
            answers.append(questions[y]['answer'])
            y+=1
            answers.append(questions[y]['answer'])
            y+=1
            answers.append(questions[y]['answer'])
            y+=1
            answers.append(questions[y]['answer'])
            y+=1
            answers.append(questions[y]['answer'])
            #print(x, y, answers)

            data = {'question': question, 'answers': answers}
            self.redis.rpush(idcache, json.dumps(data))

        pregunta = json.loads(self.redis.lpop(idcache))
        data = {
            "pruebaId": pruebaId,
            "candidatoId": candidatoId,
            "question": pregunta['question'],
            "answers": pregunta['answers']
        }
        return json.dumps(data), 200

class PruebaNext(Resource):

    def post(self, candidatoId, pruebaId):
        # 400 - En el caso que alguno de los campos no esté presente en la solicitud
        if candidatoId is None or pruebaId is None: 
            return "parameter(s) missing", 400

        idcache = pruebaId+"-"+candidatoId
        pregunta = json.loads(self.redis.lpop(idcache))
        data = {
            "pruebaId": pruebaId,
            "candidatoId": candidatoId,
            "question": pregunta['question'],
            "answers": pregunta['answers']
        }
        return json.dumps(data), 200


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