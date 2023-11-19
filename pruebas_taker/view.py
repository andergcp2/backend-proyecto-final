import json, requests, redis
from flask import request, Response, current_app
from flask_restful import Resource
#from redis_client import RedisClient

def getCandidato(endpoint, headers):
    return get(endpoint, headers)

def getPrueba(endpoint, headers):
    return get(endpoint, headers)

def getPruebaCandidato(endpoint, headers):
    return get(endpoint, headers)

def get(endpoint, headers):
    try:
        resp = requests.get(endpoint, headers = headers)
        if (resp.status_code==200):
            #return json.dumps(resp.json()), resp.status_code
            return {'msg': resp.json(), 'status_code': resp.status_code}
        #return json.dumps(resp.content), resp.status_code
        return {'msg': resp.content, 'status_code': resp.status_code} 
    except Exception as ex:
        # return (resp.json, resp.status_code, resp.headers.items())
        #return json.dumps('connection endpoint failed {} -> {}'.format(endpoint, ex)), resp.status_code
        return {'msg': 'connection endpoint failed {} -> {}'.format(endpoint, ex), 'status_code': 500}

def updatePruebaCandidato(endpoint, data, headers):
    try:
        resp = requests.post(endpoint, data=json.dumps(data), headers = headers)
        return resp
    except Exception as ex:
        return {'msg': 'connection endpoint failed {} -> {}'.format(endpoint, ex), 'status_code': 500}
        #return (resp.json, resp.status_code, resp.headers.items())

def deleteCache(key):
    self.redis.delete(key)

def setCache(key, data):
    self.redis.hset(key, mapping=data)
    #self.redis.rpush(key, json.dumps(data))

def getCache(key):
    return self.redis.hgetall(key)
    #return json.loads(self.redis.lpop(key))


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
        testing = current_app.config['TESTING']
        headers = {"Content-Type":"application/json", "Authorization": request.headers['Authorization']}

        if candidatoId is not None: 
            try:
                int(candidatoId)
            except ValueError:
                return "candidato id is not a number", 400

        if pruebaId is not None: 
            try:
                int(pruebaId)
            except ValueError:
                return "prueba id is not a number", 400

        # 400 - En el caso que alguno de los campos no esté presente en la solicitud
        if candidatoId is None or pruebaId is None: 
            return "parameter(s) missing", 400

        endpoint = format(current_app.config['CANDIDATOS_QUERY']) +"/{}".format(candidatoId)
        if not testing:
            print ("candidato-url: ", endpoint)
        resp = getCandidato(endpoint, headers)
        #print ("candidato-resp: ", endpoint, resp)
        if(resp['status_code'] != 200):
            # 404 - El candidato que va a tomar la prueba no existe
            return resp, resp['status_code'] # Response(resp['msg'], resp['status_code']) resp.headers.items()
        candidato = resp['msg']

        endpoint = format(current_app.config['PRUEBAS_QUERY']) +"/{}".format(pruebaId)
        if not testing:
            print ("prueba-url: ", endpoint)
        resp = getPrueba(endpoint, headers)
        #print ("prueba-resp: ", endpoint, resp)
        if(resp['status_code'] != 200):
            # 404 - La prueba a iniciar no existe
            return resp, resp['status_code']
        prueba = resp['msg']

        endpoint = format(current_app.config['CANDIDATOS_PRUEBAS']) +"/{}/{}".format(candidatoId, pruebaId)
        if not testing:
            print ("candidato-prueba-url: ", endpoint)
        resp = getPruebaCandidato(endpoint, headers)
        #print ("candidato-prueba-res: ", endpoint, resp)
        if(resp['status_code'] != 200):
            # 404 - El candidato no está asociado a la prueba
            return resp, resp['status_code']

        idcache = pruebaId+"-"+candidatoId
        deleteCache(idcache)

        # for x in range(0, len(prueba['questions'])):
        #     y=x
        #     answers = []
        #     question = questions[x]['question']
        #     answers.append(questions[y]['answer'])
        #     y+=1
        #     answers.append(questions[y]['answer'])
        #     y+=1
        #     answers.append(questions[y]['answer'])
        #     y+=1
        #     answers.append(questions[y]['answer'])
        #     y+=1
        #     answers.append(questions[y]['answer'])

        #     data = {'question': question, 'answers': answers}
        #     pushCache(idcache, data)

        # mango = True
        # data = {
        #     "prueba": prueba,
        #     "candidato": candidato,
        #     "questions": prueba['questions'],
        #     "totalQuestions": prueba['numQuestions']
        # }

        # print()
        # print(data)
        # if (mango):
        #     return json.dumps(data), 200

        data = {
            "pruebaId": pruebaId,
            "candidatoId": candidatoId,
            "totalQuestions": prueba['numQuestions'], 
            "numQuestion": 1, 
            # "question": pregunta['question'],
            # "answers": pregunta['answers']
        }

        #data = {'question': question, 'answers': answers}
        setCache(idcache, data)
        prueba = getCache(idcache)

        return json.dumps(data), 200


class PruebaNext(Resource):

    def post(self, candidatoId, pruebaId):
        testing = current_app.config['TESTING']
        headers = {"Content-Type":"application/json", "Authorization": request.headers['Authorization']}

        if candidatoId is not None: 
            try:
                int(candidatoId)
            except ValueError:
                return "candidato id is not a number", 400

        if pruebaId is not None: 
            try:
                int(pruebaId)
            except ValueError:
                return "prueba id is not a number", 400

        # 400 - En el caso que alguno de los campos no esté presente en la solicitud
        if candidatoId is None or pruebaId is None: 
            return "parameter(s) missing", 400

        idcache = pruebaId+"-"+candidatoId
        pregunta = getCache(idcache)
        #pregunta = json.loads(self.redis.lpop(idcache))
        data = {
            "pruebaId": pruebaId,
            "candidatoId": candidatoId,
            # "totalQuestions": prueba['numQuestions'], 
            # "numQuestion": 1, 
            # "question": pregunta['question'],
            # "answers": pregunta['answers']
        }
        return json.dumps(data), 200


class PruebaDone(Resource):

    def post(self, candidatoId, pruebaId):
        testing = current_app.config['TESTING']
        headers = {"Content-Type":"application/json", "Authorization": request.headers['Authorization']}

        if candidatoId is not None: 
            try:
                int(candidatoId)
            except ValueError:
                return "candidato id is not a number", 400

        if pruebaId is not None: 
            try:
                int(pruebaId)
            except ValueError:
                return "prueba id is not a number", 400


        # 400 - En el caso que alguno de los campos no esté presente en la solicitud
        if candidatoId is None or pruebaId is None: 
            return "parameter(s) missing", 400

        idcache = pruebaId+"-"+candidatoId
        pregunta = getCache(idcache)

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
        endpointP = format(current_app.config['CANDIDATOS_PRUEBAS'])
        resp = updatePruebaCandidato(endpointP, data, headers)
        # print("prueba: ", endpointP, resp)
        status_code = resp['status_code']
        if(status_code != 200):
            return resp['msg'], status_code

        return data, 200
