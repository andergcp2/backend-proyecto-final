import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from model import db
from view import HealthCheck, Projects, GetCompanyProjects, GetProject, SetCandidateProject

app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
if 'USERS_PATH' in os.environ:
    app.config['USERS'] = str(os.environ.get("USERS_PATH")) +'/users/me'
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://"+ str(os.environ.get("DB_USER")) +":"+ str(os.environ.get("DB_PASSWORD")) +"@"+ str(os.environ.get("DB_HOST")) +":"+ str(os.environ.get("DB_PORT")) +"/"+ str(os.environ.get("DB_NAME"))
    print("prod: ", app.config['SQLALCHEMY_DATABASE_URI'], app.config['USERS'])
    app.config['CANDIDATOS_QUERY'] = str(os.environ.get("CANDIDATOS_PATH"))    
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
    #app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://usrabc:pwdjobs@localhost:5432/abcjobs"
    app.config['CANDIDATOS_QUERY'] = 'http://abcjobs-public-alb-388103681.us-east-1.elb.amazonaws.com/candidates-qry'
    app.config['TESTING'] = True
    print("testing: ", app.config['SQLALCHEMY_DATABASE_URI'])

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(Projects, '/projects' )
api.add_resource(GetProject, '/projects/<id>')
api.add_resource(HealthCheck,'/projects/ping' )
api.add_resource(GetCompanyProjects, '/projects/companies/<companyId>')
api.add_resource(SetCandidateProject, '/projects/<projectId>/candidates/<candidatoId>')
