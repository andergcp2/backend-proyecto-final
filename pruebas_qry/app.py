import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from model import db
from view import HealthCheck, GetTests, GetTest

app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
if 'USERS_PATH' in os.environ:
    app.config['USERS'] = str(os.environ.get("USERS_PATH")) +'/users/me'
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://"+ str(os.environ.get("DB_USER")) +":"+ str(os.environ.get("DB_PASSWORD")) +"@"+ str(os.environ.get("DB_HOST_READ")) +":"+ str(os.environ.get("DB_PORT")) +"/"+ str(os.environ.get("DB_NAME"))
    print("prod: ", app.config['SQLALCHEMY_DATABASE_URI'], app.config['USERS'])
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pruebas-qry.db'
    app.config['TESTING'] = True
    print("test: ", app.config['SQLALCHEMY_DATABASE_URI'])

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(GetTests, '/tests-qry' )
api.add_resource(GetTest, '/tests-qry/<string:id>' )
api.add_resource(HealthCheck,'/tests-qry/ping' )
#jwt = JWTManager(app)
