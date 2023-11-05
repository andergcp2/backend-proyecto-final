from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from datetime import datetime

db = SQLAlchemy()

class Candidate(db.Model):
    __tablename__ = "candidate"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    idType = db.Column(db.String(5))
    identification = db.Column(db.String(20))
    email = db.Column(db.String(100))
    phone = db.Column(db.Integer)
    country = db.Column(db.String(200))
    city = db.Column(db.String(200))
    address = db.Column(db.String(255))
    profession = db.Column(db.String(200))
    softSkills = db.relationship("SoftSkills", back_populates="candidate")
    technicalSkills = db.relationship("TechnicalSkills", back_populates="candidate")
    username = db.Column(db.String(100))
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return f'<Candidate "{self.name, self.softSkills}">'

class SoftSkills(db.Model):
    __tablename__ = "soft_skills"
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidate.id"))
    skill = db.Column(db.String(50))
    candidate = db.relationship("Candidate", back_populates="softSkills")
    def __repr__(self):
        return f'<SoftSkills "{self.skill}">'

class TechnicalSkills(db.Model):
    __tablename__ = "technical_skills"
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidate.id"))
    skill = db.Column(db.String(50))
    candidate = db.relationship("Candidate", back_populates="technicalSkills")
    def __repr__(self):
        return f'<TechnicalSkills "{self.skill}">'

class SoftSkillsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SoftSkills
        load_instance = True

class TechnicalSkillsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TechnicalSkills
        load_instance = True

class CandidateSchema(SQLAlchemyAutoSchema):
    softSkills = fields.Nested(SoftSkillsSchema, many=True, only=('skill',))
    technicalSkills = fields.Nested(TechnicalSkillsSchema, many=True, only=('skill',))
    class Meta:
        model = Candidate
        load_instance = True
        