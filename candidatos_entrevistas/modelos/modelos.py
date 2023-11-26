from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from datetime import datetime

db = SQLAlchemy()

class InterviewCandidate(db.Model):
    __tablename__ = "candidateinterview"
    interviewId = db.Column(db.Integer, primary_key=True)
    candidateId = db.Column(db.Integer)
    companyId = db.Column(db.Integer)
    projectId = db.Column(db.Integer)
    profileId = db.Column(db.Integer)
    interviewDate = db.Column(db.DateTime)
    topic = db.Column(db.String(50))
    score = db.Column(db.Integer)
    status = db.Column(db.Enum("CREADA", "FINALIZADA", name='status'))
    comment = db.Column(db.String(250))
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
class InterviewCandidateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = InterviewCandidate
        load_instance = True
        