from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from datetime import datetime

db = SQLAlchemy()

class CandidateTest(db.Model):
    __tablename__ = "candidatetest"
    id = db.Column(db.Integer, primary_key=True)
    idcandidate = db.Column(db.Integer)
    idtest = db.Column(db.Integer)
    maxdatepresent = db.Column(db.Date)
    presentationdate = db.Column(db.DateTime)
    qualificationtest = db.Column(db.Integer)
    testestatus = db.Column(db.Enum("ASIGNADA", "EN CURSO", "CANCELADA","FINALIZADA", name='statusTest'))
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
class CandidateTestSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CandidateTest
        load_instance = True
        