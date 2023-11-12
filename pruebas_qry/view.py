import json, requests
from flask import request, current_app
from flask_restful import Resource
from model import db, Test, Question, Answer, Profile, TechnicalSkill 
from model import TestSchema, QuestionSchema, AnswerSchema, ProfileSchema, TechnicalSkillSchema

test_schema = TestSchema()
question_schema = QuestionSchema()
answer_schema = AnswerSchema()
techskill_schema = TechnicalSkillSchema()
profile_schema = ProfileSchema()

class HealthCheck(Resource):
    def get(self):
        return "ok"

class GetTests(Resource):

    def get(self):

        tests = db.session.query(Test).order_by(Test.createdAt).all()
        return [test_schema.dump(t) for t in tests]

        # tests = db.session.query(Test, Question, Answer, Profile, TechnicalSkill).filter(Test.id==Profile.testId).filter(Test.id==TechnicalSkill.testId).filter(Test.id==Question.testId).filter(Question.id==Answer.questionId).order_by(Test.createdAt).all()
        # data = [{'test': test_schema.dump(t[0]), 'question': question_schema.dump(t[1]), 'answer': answer_schema.dump(t[2])} for t in tests]
        # return json.dumps(data)
        
class GetTest(Resource):

    def get(self, id):
        if id is not None: 
            try:
                int(id)
            except ValueError:
                return "the test id is not a number", 412

        test = Test.query.filter(Test.id == id).first()
        if test is None:
            return "the test with the given id was not found", 404

        return test_schema.dump(test)
