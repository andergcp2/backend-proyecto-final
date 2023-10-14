import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from view import HealthCheck, PruebaInit, PruebaNext, PruebaDone

app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True

if 'USERS_PATH' in os.environ:
    #app.config['USERS']  = str(os.environ.get("USERS_PATH")) +'/users/me'
    # app.config['CANDIDATOS_QUERY'] = str(os.environ.get("CANQ_PATH")) +":"+ str(os.environ.get("CANQ_PORT")) +"/candidates-query"
    # app.config['PRUEBAS_QUERY'] = str(os.environ.get("PRUQ_PATH")) +":"+ str(os.environ.get("PRUQ_PORT")) +"/pruebas-query"
    # app.config['PREGUNTAS_QUERY'] = str(os.environ.get("PREQ_PATH")) +":"+ str(os.environ.get("PREQ_PORT")) +"/preguntas-query"

    app.config['CANDIDATOS_QUERY'] = 'http://candidatos-query:3696/candidates-query'
    app.config['PRUEBAS_QUERY'] = 'http://pruebas-query:3696/pruebas-query'
    app.config['PREGUNTAS_QUERY'] = 'http://preguntas-query:3696/preguntas-query'
    print("CANDIDATOS_QUERY: ", app.config['CANDIDATOS_QUERY'])
    print("PRUEBAS_QUERY: ", app.config['PRUEBAS_QUERY'])
    print("PREGUNTAS_QUERY: ", app.config['PREGUNTAS_QUERY'])


    app.config['ELASTICACHE_HOST']  = 'jobs-cache'
    app.config['ELASTICACHE_PORT']  = '6379'
    # app.config['ELASTICACHE_HOST']  = str(os.environ.get("ELASTICACHE_HOST"))
    # app.config['ELASTICACHE_PORT']  = str(os.environ.get("ELASTICACHE_PORT"))
    print("ELASTICACHE_HOST: ", app.config['ELASTICACHE_HOST'])
    print("ELASTICACHE_PORT: ", app.config['ELASTICACHE_PORT'])


else:
    app.config['CANDIDATOS_QUERY'] = 'http://localhost:36961/candidates-query'
    app.config['PRUEBAS_QUERY'] = 'http://localhost:36962/pruebas-query'
    app.config['PREGUNTAS_QUERY'] = 'http://localhost:36963/preguntas-query'

    app.config['ELASTICACHE_HOST']  = 'localhost'
    app.config['ELASTICACHE_PORT']  = 6379

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pruebas.db'
    app.config['TESTING'] = True
    print("test: ", app.config['SQLALCHEMY_DATABASE_URI'])

app_context = app.app_context()
app_context.push()

cors = CORS(app)
api = Api(app)

api.add_resource(PruebaInit, '/pruebas/init/<string:candidatoId>/<string:pruebaId>')
api.add_resource(PruebaNext, '/pruebas/next/<string:candidatoId>/<string:pruebaId>')
api.add_resource(PruebaDone, '/pruebas/done/<string:candidatoId>/<string:pruebaId>')
api.add_resource(HealthCheck, '/pruebas/ping')  
