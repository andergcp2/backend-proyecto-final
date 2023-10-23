from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from datetime import datetime

db = SQLAlchemy()

class Company(db.Model):
    __tablename__ = "company"
    id = db.Column(db.Integer, primary_key=True)
    idType = db.Column(db.String(20))
    idNumber = db.Column(db.Integer)
    companyName = db.Column(db.String(50))
    industry = db.Column(db.String(30))
    email = db.Column(db.String(100))
    phone = db.Column(db.Integer)
    address = db.Column(db.String(255))
    country = db.Column(db.String(200))
    city = db.Column(db.String(200))
    reprName = db.Column(db.String(100))
    reprIdType = db.Column(db.String(20))
    reprIdNumber = db.Column(db.Integer)
    #userId = db.Column(db.Integer)
    #plannedStartDate = db.Column(db.DateTime)
    #plannedEndDate = db.Column(db.DateTime)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class CompanySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Company
        load_instance = True