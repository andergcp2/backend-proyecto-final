from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from datetime import datetime

db = SQLAlchemy()

class InterviewCandidate(db.Model):
    __tablename__ = "candidateinterview"
    id = db.Column(db.Integer, primary_key=True)
    idcandidate = db.Column(db.Integer)
    idinterview = db.Column(db.Enum("INDIVIDUAL SP", "GRUPAL", "JEFE", name='idInterview'))
    summonsdate = db.Column(db.DateTime)
    presentationdate = db.Column(db.DateTime)
    qualificationtest = db.Column(db.Integer)
    interviewstatus = db.Column(db.Enum("PROGRAMADA", "EN CURSO", "CANCELADA","FINALIZADA", name='interviewstatus'))
    interviewer = db.Column(db.String(100))
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
class InterviewCandidateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = InterviewCandidate
        load_instance = True
        