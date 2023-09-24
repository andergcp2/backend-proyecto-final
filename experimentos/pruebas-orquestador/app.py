import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from view import HealthCheck, PruebaInit, PruebaNext, PruebaDone

app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True

#app.config['USERS']  = str(os.environ.get("USERS_PATH")) +'/users/me'
app.config['CANDIDATOS_QUERY']  = str(os.environ.get("CANDIDATOS_QUERY_PATH"))
app.config['PRUEBAS_QUERY'] = str(os.environ.get("PRUEBAS_QUERY_PATH"))
app.config['PREGUNTAS_QUERY'] = str(os.environ.get("PREGUNTAS_QUERY_PATH"))

app_context = app.app_context()
app_context.push()

cors = CORS(app)

api = Api(app)

api.add_resource(HealthCheck, '/pruebas/orquestador/ping')  
api.add_resource(PruebaInit, '/pruebas/orquestador/<string:id>/<string:id>')
api.add_resource(PruebaNext, '/pruebas/orquestador/<string:id>/<string:id>')
api.add_resource(PruebaDone, '/pruebas/orquestador/<string:id>/<string:id>')
