import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from view import HealthCheck, PruebaInit, PruebaNext, PruebaDone

app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True

if 'USERS_PATH' in os.environ:
    #app.config['USERS']  = str(os.environ.get("USERS_PATH")) +'/users/me'
    app.config['CANDIDATOS_QUERY'] = str(os.environ.get("CANDIDATOS_QUERY_PATH"))
    app.config['CANDIDATOS_PORT'] = str(os.environ.get("CANDIDATOS_QUERY_PORT"))
    app.config['PRUEBAS_QUERY'] = str(os.environ.get("PRUEBAS_QUERY_PATH"))
    app.config['PRUEBAS_PORT'] = str(os.environ.get("PRUEBAS_QUERY_PORT"))
    app.config['PREGUNTAS_QUERY'] = str(os.environ.get("PREGUNTAS_QUERY_PATH"))
    app.config['PREGUNTAS_PORT'] = str(os.environ.get("PREGUNTAS_QUERY_PORT"))

    app.config['ELASTICACHE_HOST']  = str(os.environ.get("ELASTICACHE_HOST"))
    app.config['ELASTICACHE_PORT']  = str(os.environ.get("ELASTICACHE_PORT"))
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
