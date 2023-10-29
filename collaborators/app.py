import os
from flask import Flask
from flask_cors import CORS
from flask_restful import  Api
from modelos import db
from vistas import VistaPing, VistaCollaborators

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
if 'USERS_PATH' in os.environ:
    app.config['USERS'] = 'http://'+ str(os.environ.get("USERS_PATH")) +":"+ str(os.environ.get("USERS_PORT")) +'/users/me'
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://"+ str(os.environ.get("DB_USER")) +":"+ str(os.environ.get("DB_PASSWORD")) +"@"+ str(os.environ.get("DB_HOST")) +":"+ str(os.environ.get("DB_PORT")) +"/"+ str(os.environ.get("DB_NAME"))
    print("prod: ", app.config['SQLALCHEMY_DATABASE_URI'], app.config['USERS'])
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///collaborators.db'
    app.config['TESTING'] = True
    print("test: ", app.config['SQLALCHEMY_DATABASE_URI'])

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaCollaborators, '/collaborators')
api.add_resource(VistaPing, '/collaborators/ping')

