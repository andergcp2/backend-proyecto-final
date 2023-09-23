from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Candidate(db.Model):
    __tablename__ = "candidate"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@property
def createdAt(self):
    return self.createdAt.isoformat()

class TestCandidate(db.Model):
    __tablename__ = "test_candidate"
    id = db.Column(db.Integer, primary_key=True)
    id_candidate = db.Column(db.Integer, db.ForeignKey('candidate.id'))
    id_test = db.Column(db.Integer)
    result = db.Column(db.Float)
    presented = db.Column(db.Boolean, default=False)
    presentedAt = db.Column(db.DateTime)

@property
def presentedAt(self):
    return self.presentedAt.isoformat()

class CandidateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Candidate
        load_instance = True

class TestCandidateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TestCandidate
        include_relationships = True
        include_fk = True
        load_instance = True
