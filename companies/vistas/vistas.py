import requests
from flask import request, current_app
from flask_restful import Resource
from datetime import datetime

from modelos import db, Company, CompanySchema

company_schema = CompanySchema()

class VistaPing(Resource):
    def get(self):
        return "PONG", 200