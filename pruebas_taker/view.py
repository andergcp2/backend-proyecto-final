import json, requests, redis
from flask import request, current_app, jsonify
from flask_restful import Resource

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

def deleteCache(self, key):
    self.redis.delete(key)
    print("delete-cache")

def setCache(self, key, data):
    self.redis.set(key, json.dumps(data))
    #self.redis.hset(key, mapping=data)
    #self.redis.hset(key, mapping=json.dumps(data))

def getCache(self, key):
    return json.loads(self.redis.get(key))
    # return self.redis.hgetall(key)
    #return json.loads(self.redis.lpop(key))

def setupCache(self, fase):
    print("setup-cache")
    print(fase, current_app.config['CACHE_HOST'], current_app.config['CACHE_PORT'] )
    #self.redis = redis.Redis(host=current_app.config['CACHE_HOST'], port=current_app.config['CACHE_PORT'], decode_responses=True, ssl=True) #encoding="utf-8"
    pool = redis.ConnectionPool(host=current_app.config['CACHE_HOST'], port=current_app.config['CACHE_PORT'], db=0)
    self.redis = redis.Redis(connection_pool=pool)
    try:
        cache_is_working = self.redis.ping()    
        logging.info(fase, "connected to redis")
    except Exception as ex:
        print(fase, 'exception: host could not be accessed: {}'.format(ex))


class HealthCheck(Resource):
    def get(self):
        #print("check-ok")
        return "ok"

class PruebaInit(Resource):
    def __init__(self) -> None:
        setupCache(self, 'prueba-init')
        super().__init__()

    def post(self, candidatoId, pruebaId):
        testing = current_app.config['TESTING']
        headers = {"Content-Type":"application/json"} # , "Authorization": request.headers['Authorization']

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

        # 400 si alguno de los parametros no esta presente
        if candidatoId is None or pruebaId is None: 
            return "parameter(s) missing", 400

        endpoint = format(current_app.config['CANDIDATOS_QUERY']) +"/{}".format(candidatoId)
        if not testing:
            print ("candidato-url: ", endpoint)
        resp = getCandidato(endpoint, headers)
        if(resp['status_code'] != 200):
            # 404 - El candidato que va a tomar la prueba no existe
            return resp, resp['status_code'] # Response(resp['msg'], resp['status_code']) resp.headers.items()
        candidato = resp['msg']

        endpoint = format(current_app.config['PRUEBAS_QUERY']) +"/{}".format(pruebaId)
        if not testing:
            print ("prueba-url: ", endpoint)
        resp = getPrueba(endpoint, headers)
        if(resp['status_code'] != 200):
            # 404 - La prueba a iniciar no existe
            return resp, resp['status_code']
        prueba = resp['msg']

        endpoint = format(current_app.config['CANDIDATOS_PRUEBAS']) +"/{}/{}".format(candidatoId, pruebaId)
        if not testing:
            print ("candidato-prueba-url: ", endpoint)
        resp = getPruebaCandidato(endpoint, headers)
        if(resp['status_code'] != 200):
            # 404 - El candidato no está asociado a la prueba
            return resp, resp['status_code']

        data = {
            'pruebaId': prueba['id'],
            'candidatoId': candidato['id'],
            "totalQuestions": prueba['numQuestions'],
            "numQuestion": 1, 
            "answersOK": 0, 
            "prueba": prueba,
            "candidato": candidato,
        }

        idcache = pruebaId+"-"+candidatoId
        deleteCache(self, idcache)
        setCache(self, idcache, data)
        test = getCache(self, idcache)

        answers = []
        respuestas = prueba['questions'][0]['answers']
        for x in range(len(respuestas)):
            answers.append({"id": respuestas[x]['id'], "answer": respuestas[x]['answer']})

        resp_init = {
            'pruebaId': prueba['id'],
            'candidatoId': candidato['id'],
            'question': {'id': prueba['questions'][0]['id'], 'question': prueba['questions'][0]['question']},
            'answers': answers,
            'totalQuestions': prueba['numQuestions'], 
            'numQuestion': 1, 
        }
 
        #print(type(resp_init), resp_init)
        #return json.dumps(resp_init), 200
        return jsonify(resp_init)

class PruebaNext(Resource):
    def __init__(self) -> None:
        setupCache(self, 'prueba-next')
        super().__init__()
       
    def post(self, candidatoId, pruebaId):
        testing = current_app.config['TESTING']
        headers = {"Content-Type":"application/json"} # , "Authorization": request.headers['Authorization']

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

        # 400 si alguno de los parametros no esta presente
        if candidatoId is None or pruebaId is None: 
            return "parameter(s) missing", 400

        data = request.get_json()
        totalQuestions = numQuestion = questionId = answerId = None

        if "totalQuestions" not in data or data["totalQuestions"] is None:
            return "total questions is required", 400
        elif "numQuestion" not in data or data["numQuestion"] is None:
            return "number of question is required", 400
        elif "questionId" not in data or data["questionId"] is None:
            return "question id is required", 400
        elif "answerId" not in data or data["answerId"] is None:
            return "answer id is required", 400

        totalQuestions = data["totalQuestions"]
        numQuestion = data["numQuestion"]
        questionId = data["questionId"]
        answerId = data["answerId"]

        idcache = pruebaId+"-"+candidatoId
        test = getCache(self, idcache)
        # 404 si no existen los parametros como llave en la cache
        if(test is None):
            return "this test was not started by candidate", 404

        # 412 no debe ser la ultima pregunta
        if (numQuestion == totalQuestions):
            return "this question should not be the last question", 412

        idx = numQuestion
        numQuestion +=1    

        respuestas = test['prueba']['questions'][idx-1]['answers']
        for x in range(len(respuestas)):
            if(respuestas[x]['id'] == answerId and respuestas[x]['correct']):
                test['answersOK'] = test['answersOK'] +1
                setCache(self, idcache, test)
                print("question ok ", idx)

        answers = []
        respuestas = test['prueba']['questions'][idx]['answers']
        for x in range(len(respuestas)):
            answers.append({"id": respuestas[x]['id'], "answer": respuestas[x]['answer']})

        resp_next = {
            'pruebaId': test['prueba']['id'],
            'candidatoId': test['candidato']['id'],
            'question': {'id': test['prueba']['questions'][idx]['id'], 'question': test['prueba']['questions'][idx]['question']},
            'answers': answers,
            'totalQuestions': test['prueba']['numQuestions'], 
            'numQuestion': numQuestion, 
        }

        return jsonify(resp_next)


class PruebaDone(Resource):
    def __init__(self) -> None:
        setupCache(self, 'prueba-done')
        super().__init__()

    def post(self, candidatoId, pruebaId):
        testing = current_app.config['TESTING']
        headers = {"Content-Type":"application/json"} # , "Authorization": request.headers['Authorization']

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

        # 400 si alguno de los parametros no esta presente
        if candidatoId is None or pruebaId is None: 
            return "parameter(s) missing", 400

        data = request.get_json()
        totalQuestions = numQuestion = questionId = answerId = None

        if "totalQuestions" not in data or data["totalQuestions"] is None:
            return "total questions is required", 400
        elif "numQuestion" not in data or data["numQuestion"] is None:
            return "number of question is required", 400
        elif "questionId" not in data or data["questionId"] is None:
            return "question id is required", 400
        elif "answerId" not in data or data["answerId"] is None:
            return "answer id is required", 400

        totalQuestions = data["totalQuestions"]
        numQuestion = data["numQuestion"]
        questionId = data["questionId"]
        answerId = data["answerId"]

        idcache = pruebaId+"-"+candidatoId
        test = getCache(self, idcache)
        # 404 si no existen los parametros como llave en la cache
        if(test is None):
            return "this test was not started by candidate", 404

        # 412 no debe ser la ultima pregunta
        if (numQuestion != totalQuestions):
            return "this question should be the last question", 412

        idx = numQuestion
        numQuestion +=1    

        respuestas = test['prueba']['questions'][idx-1]['answers']
        for x in range(len(respuestas)):
            if(respuestas[x]['id'] == answerId and respuestas[x]['correct']):
                test['answersOK'] = test['answersOK'] +1
                setCache(self, idcache, test)
                print("question ok ", idx)

        resp_done = {
            'pruebaId': test['prueba']['id'],
            'candidatoId': test['candidato']['id'],
            'totalQuestions': test['prueba']['numQuestions'], 
            'answersOK': test['answersOK'], 
            'result': round (test['answersOK'] / test['prueba']['numQuestions'], 2)
        }

        # endpointP = format(current_app.config['CANDIDATOS_PRUEBAS'])
        # resp = updatePruebaCandidato(endpointP, datresp_donea, headers)
        # # print("prueba: ", endpointP, resp)
        # status_code = resp['status_code']
        # if(status_code != 200):
        #     return resp['msg'], status_code

        return jsonify(resp_done)
