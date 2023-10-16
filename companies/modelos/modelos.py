from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from datetime import datetime

db = SQLAlchemy()

class Company(db.Model):
    __tablename__ = "company"
    id = db.Column(db.Integer, primary_key=True)
    tipoIde = db.Column(db.String(20))
    numeroIde = db.Column(db.String(30))
    razonsocial = db.Column(db.String(50))
    sector = db.Column(db.String(30))
    correo = db.Column(db.String(100))
    telefono = db.Column(db.String(30))
    pais = db.Column(db.String(200))
    ciudad = db.Column(db.String(200))
    direccion = db.Column(db.String(255))
    representante = db.Column(db.String(100))
    tpidrepresentante = db.Column(db.String(20))
    numidrepresentante = db.Column(db.String(50))
    #userId = db.Column(db.Integer)
    #plannedStartDate = db.Column(db.DateTime)
    #plannedEndDate = db.Column(db.DateTime)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class CompanySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Company
        load_instance = True