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
    #paisId = db.Column(db.Integer)
    #ciudadId = db.Column(db.Integer)
    direccion = db.Column(db.IntegString(255))
    #userId = db.Column(db.Integer)
    #plannedStartDate = db.Column(db.DateTime)
    #plannedEndDate = db.Column(db.DateTime)
    #createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class PostSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Company
        load_instance = True