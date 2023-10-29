from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from datetime import datetime

db = SQLAlchemy()

class Collaborator(db.Model):
    __tablename__ = "collaborator"
    id = db.Column(db.Integer, primary_key=True)
    idType = db.Column(db.String(20))
    idNumber = db.Column(db.Integer)
    collaboratorName = db.Column(db.String(50))
    collaboratorLastName = db.Column(db.String(50))
    email = db.Column(db.String(100))
    phone = db.Column(db.Integer)
    address = db.Column(db.String(255))
    role = db.Column(db.String(200))
    position = db.Column(db.String(200))
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class CollaboratorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Collaborator
        load_instance = True