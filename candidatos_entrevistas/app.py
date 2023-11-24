import os
from flask import Flask
from flask_cors import CORS
from flask_restful import  Api
from modelos import db
from vistas import VistaPing, VistaCandidateInterview, VistaCandidateInterviewSearch, VistaTestsAssignedToCandidates, VistaUpdateInterviewCandidate

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
if 'USERS_PATH' in os.environ:
    app.config['USERS'] = os.environ.get("USERS_PATH")
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://"+ str(os.environ.get("DB_USER")) +":"+ str(os.environ.get("DB_PASSWORD")) +"@"+ str(os.environ.get("DB_HOST")) +":"+ str(os.environ.get("DB_PORT")) +"/"+ str(os.environ.get("DB_NAME"))
    app.config['TEST_QRY_URL'] = str(os.environ.get("PRUEBAS_QUERY"))
    print("prod: ", app.config['SQLALCHEMY_DATABASE_URI'], app.config['USERS'])
else:
    app.config['USERS'] = 'https://tpy2fq7k1h.execute-api.us-east-1.amazonaws.com/test/signin'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///candidates.db'
    app.config['TESTING'] = True
    app.config['TEST_QRY_URL'] = "http://abcjobs-public-alb-388103681.us-east-1.elb.amazonaws.com/tests-qry"
    print("test: ", app.config['SQLALCHEMY_DATABASE_URI'])

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaCandidateInterview, '/interviews')
api.add_resource(VistaPing, '/interviews/ping')
api.add_resource(VistaCandidateInterviewSearch, '/interviews/<companyId>/<projectId>')
api.add_resource(VistaTestsAssignedToCandidates, '/interviews/candidate/<candidateId>')
api.add_resource(VistaUpdateInterviewCandidate, '/interviews/<interviewId>')
