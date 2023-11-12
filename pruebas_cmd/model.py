from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Test(db.Model):
    __tablename__ = "tests"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    numQuestions = db.Column(db.Integer)
    minLevel = db.Column(db.Integer)
    profiles = db.relationship('Profile', cascade='all, delete, delete-orphan')
    techSkills = db.relationship("TechnicalSkill", cascade='all, delete, delete-orphan')
    questions = db.relationship("Question", cascade='all, delete, delete-orphan')
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return f'<Test "{self.id, self.name, self.minLevel, self.numQuestions}">'    

@property
def createdAt(self):
    return self.createdAt.isoformat()

class Profile(db.Model):
    __tablename__ = "tests_profiles"
    id = db.Column(db.Integer, primary_key=True)
    testId = db.Column(db.Integer, db.ForeignKey("tests.id"))
    profile = db.Column(db.String(50))
    #test = db.relationship("Test", back_populates="profiles")
    def __repr__(self):
        return f'<ProfileTest "{self.testId, self.profile}">'

class TechnicalSkill(db.Model):
    __tablename__ = "tests_technical_skills"
    id = db.Column(db.Integer, primary_key=True)
    testId = db.Column(db.Integer, db.ForeignKey("tests.id"))
    skill = db.Column(db.String(50))
    #test = db.relationship("Test", back_populates="technicalSkills")
    def __repr__(self):
        return f'<TechnicalSkillsTest "{self.testId, self.skill}">'

class Question(db.Model):
    __tablename__ = "tests_questions"
    id = db.Column(db.Integer, primary_key=True)
    testId = db.Column(db.Integer, db.ForeignKey('tests.id'))
    question = db.Column(db.String(512))
    level = db.Column(db.Integer)
    url = db.Column(db.String(256))
    answers = db.relationship("Answer", cascade='all, delete, delete-orphan')
    def __repr__(self):
        return f'<Question "{self.testId, self.level, self.question, self.answers}">'

class Answer(db.Model):
    __tablename__ = "tests_answers"
    id = db.Column(db.Integer, primary_key=True)
    questionId = db.Column(db.Integer, db.ForeignKey('tests_questions.id'))
    answer = db.Column(db.String(240))
    correct = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return f'<Answer "{self.questionId, self.answer, self.correct}">'

class TestSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Test
        include_relationships = True
        load_instance = True

class TechnicalSkillSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TechnicalSkill
        include_relationships = True
        include_fk = True
        load_instance = True

class ProfileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Profile
        include_relationships = True
        include_fk = True
        load_instance = True

class QuestionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Question
        include_relationships = True
        include_fk = True
        load_instance = True

class AnswerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Answer
        include_relationships = True
        include_fk = True
        load_instance = True
