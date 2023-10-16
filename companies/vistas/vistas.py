import requests
from flask import request, current_app
from flask_restful import Resource
from datetime import datetime

from modelos import db, Company, CompanySchema

company_schema = CompanySchema()

#Funciones Comunes
def validacionString(campo, lonmin, lonmax):
    if (len(campo)>=lonmin) and (len(campo)<=lonmax):
        resultado = True
    else:
        resultado = False
    return resultado

class VistaPing(Resource):
    def get(self):
        return "PONG", 200
    
class VistaCompany(Resource):

    def get(self):
        #Validar si requiere token
        return [company_schema.dump(company) for company in Company.query.all()]
    
    def post(self):
        data = request.get_json()
        if "tipoIde" not in data or "numeroIde" not in data or "razonsocial" not in data or "sector" not in data or "correo" not in data or "telefono" not in data or "direccion" not in data or "pais" not in data or "ciudad" not in data or "representante" not in data or "tpidrepresentante" not in data or "numidrepresentante" not in data:
            return "Campos obligatorios sin diligenciar", 400
        if validacionString(request.json['tipoIde'],1,20) and validacionString(request.json['numeroIde'],3,30) and validacionString(request.json['razonsocial'],3,50) and validacionString(request.json['sector'],3,30) and validacionString(request.json['correo'],3,30) and validacionString(request.json['telefono'],3,30) and validacionString(request.json['direccion'],3,50) and validacionString(request.json['pais'],3,50) and validacionString(request.json['ciudad'],3,50) and validacionString(request.json['representante'],3,50) and validacionString(request.json['tpidrepresentante'],3,50) and validacionString(request.json['numidrepresentante'],3,50):
            tipoIde = request.json['tipoIde']
            numeroIde = request.json['numeroIde']  
            razonsocial = request.json['razonsocial']
            sector = request.json['sector']
            correo = request.json['correo']
            telefono = request.json['telefono']
            direccion = request.json['direccion']
            pais = request.json['pais']
            ciudad = request.json['ciudad']
            representante = request.json['representante']
            tpidrepresentante = request.json['tpidrepresentante']
            numidrepresentante = request.json['numidrepresentante']
            #pendiente validaciones no crear empresa repetida
       
            nuevo_company = Company(tipoIde=tipoIde,
                                    numeroIde=numeroIde,
                                    razonsocial=razonsocial,
                                    sector=sector,
                                    correo=correo,
                                    telefono=telefono,
                                    direccion=direccion,
                                    pais=pais,
                                    ciudad=ciudad,
                                    representante=representante,
                                    tpidrepresentante=tpidrepresentante,
                                    numidrepresentante=numidrepresentante
                                    )
            db.session.add(nuevo_company)
            db.session.commit()
            return company_schema.dump(nuevo_company), 201
        else:
            return "Campos no cumplen requisitos minimos", 400