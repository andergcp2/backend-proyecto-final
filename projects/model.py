#from enum import Enum
#from email.policy import default
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Project(db.Model):
    __tablename__ = "project"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    type = db.Column(db.String(50))
    leader = db.Column(db.String(50))
    role = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(50))
    countryId = db.Column(db.String(2))
    cityId = db.Column(db.Integer)
    address = db.Column(db.String(50))
    companyId = db.Column(db.Integer)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    profiles = db.relationship('Profile', cascade='all, delete, delete-orphan')

    # def __repr__(self):
    #     return f'<Project "{self.id}, {self.name}, {self.type}, {self.leader}, {self.role}, {self.phone}, {self.email}, {self.countryId}, {self.cityId}, {self.address}, {self.companyId}, {self.createdAt}">'

@property
def createdAt(self):
    return self.createdAt.isoformat()

class Profile(db.Model):
    __tablename__ = "profile"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    profession = db.Column(db.String(50))
    projectId = db.Column(db.Integer, db.ForeignKey('project.id'))
    softskills = db.relationship('SoftSkillProfile', cascade='all, delete, delete-orphan')
    techskills = db.relationship('TechSkillProfile', cascade='all, delete, delete-orphan')
    tests = db.relationship('TestProfile', cascade='all, delete, delete-orphan')

    # def __repr__(self):
    #     return f'<Profile "{self.id}, {self.name}, {self.profession}, {self.projectId}">'

class SoftSkillProfile(db.Model):
    __tablename__ = "softskill_profile"
    id = db.Column(db.Integer, primary_key=True)
    skillId = db.Column(db.Integer) # id skill microservice 
    profileId = db.Column(db.Integer, db.ForeignKey('profile.id'))

    # def __repr__(self):
    #     return f'<SkillProfile "{self.id}, {self.skillId}, {self.profileId}">'

class TechSkillProfile(db.Model):
    __tablename__ = "techskill_profile"
    id = db.Column(db.Integer, primary_key=True)
    skillId = db.Column(db.Integer) # id skill microservice 
    profileId = db.Column(db.Integer, db.ForeignKey('profile.id'))

    # def __repr__(self):
    #     return f'<SkillProfile "{self.id}, {self.skillId}, {self.profileId}">'    

class TestProfile(db.Model):
    __tablename__ = "test_profile"
    id = db.Column(db.Integer, primary_key=True)
    testId = db.Column(db.Integer) # id tests microservice 
    profileId = db.Column(db.Integer, db.ForeignKey('profile.id'))

    # def __repr__(self):
    #     return f'<TestProfile "{self.id}, {self.testId}, {self.profileId}">'

# queries: 
# customer = session.query(Customer).get(1)
# orders = customer.orders

class ProjectCandidate(db.Model):
    __tablename__ = "project_candidate"
    id = db.Column(db.Integer, primary_key=True)
    candidateId = db.Column(db.Integer)
    projectId = db.Column(db.Integer, db.ForeignKey('project.id'))
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class CandidateEvaluation(db.Model):
    __tablename__ = "project_candidate_evaluation"
    id = db.Column(db.Integer, primary_key=True)
    candidateId = db.Column(db.Integer)
    projectId = db.Column(db.Integer, db.ForeignKey('project.id'))
    score = db.Column(db.Integer)
    comments = db.Column(db.String(250))
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class ProjectSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        include_relationships = True
        include_fk = True
        load_instance = True
    # profiles = fields.List(fields.Nested(ProfileSchema()))
    profiles = fields.Nested("ProfileSchema", only=("id", "name"), many=True)

class ProfileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Profile
        include_relationships = True
        include_fk = True
        load_instance = True
    softskills = fields.Nested("SoftSkillProfileSchema", only=("skillId", "profileId"), many=True)
    techskills = fields.Nested("TechSkillProfileSchema", only=("skillId", "profileId"), many=True)
    tests = fields.Nested("TestProfileSchema", only=("testId", "profileId"), many=True) 

class SoftSkillProfileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SoftSkillProfile
        include_relationships = True
        include_fk = True
        load_instance = True

class TechSkillProfileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TechSkillProfile
        include_relationships = True
        include_fk = True
        load_instance = True        

class TestProfileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TestProfile
        include_relationships = True
        include_fk = True
        load_instance = True

class ProjectCandidateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ProjectCandidate
        #include_relationships = True
        include_fk = True
        load_instance = True

class CandidateEvaluationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CandidateEvaluation
        #include_relationships = True
        include_fk = True
        load_instance = True

