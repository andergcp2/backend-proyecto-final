import os, json, requests
from flask import request, current_app
from flask_restful import Resource
from werkzeug.utils import secure_filename
from model import db, Test, TechnicalSkill, Profile, Question, Answer, TestSchema
# TechnicalSkillSchema, ProfileSchema, QuestionSchema, AnswerSchema

test_schema = TestSchema()
# skill_schema = TechnicalSkillSchema()
# profile_schema = ProfileSchema()
# question_schema = QuestionSchema()
# answer_schema = AnswerSchema()

class HealthCheck(Resource):
    def get(self):
        return "ok"

class CreateTest(Resource):

    def post(self):
        # resp = validate_token(request.headers)
        # if(resp['status_code'] != 200):
        #     return resp['msg'], resp['status_code']

        filename = None
        if 'file' not in request.files:
            return "Test was not created - file missing", 400

        file = request.files['file']
        if file.filename == '':
            return "Test was not created - no selected file", 400

        filename = secure_filename(file.filename)
        ext = os.path.splitext(filename)[-1].lower()
        #print("-> ", filename, ext)

        if ".json" != ext:
            return "Test was not created - extension not supported", 400

        #data = request.get_json()
        data = json.load(file)
        name = type = numQuestions = minLEvel = profiles = techSkills = questions = None

        if "name" not in data or data["name"] is None:
            return "Test was not created - name is required", 400
        elif "numQuestions" not in data or data["numQuestions"] is None:
            return "Test was not created - number of questions is required", 400
        elif "minLevel" not in data or data["minLevel"] is None:
            return "Test was not created - minimun level is required", 400
        elif "profiles" not in data or data["profiles"] is None:
            return "Test was not created - profiles are required", 400
        elif "techSkills" not in data or data["techSkills"] is None:
            return "Test was not created - technical skills are required", 400
        elif "questions" not in data or data["questions"] is None:
            return "Test was not created - questions are required", 400

        for item in data["profiles"]:
            if "profile" not in item or item["profile"] is None:
                return "Test was not created - profile is required", 400

        for item in data["techSkills"]:
            if "skill" not in item or item["skill"] is None:
                return "Test was not created - skill is required", 400

        for item in data["questions"]:
            if "question" not in item or item["question"] is None:
                return "Test was not created - question is required", 400
            elif "level" not in item or item["level"] is None:
                return "Test was not created - level's question is required", 400
            elif "url" not in item or item["url"] is None:
                return "Test was not created - url's question is required", 400
            elif "answers" not in item or item["answers"] is None:
                return "Test was not created - answers' question are required", 400
            for item_answer in item["answers"]:
                if "answer" not in item_answer or item_answer["answer"] is None:
                    return "Test was not created - answer is required", 400
                elif "correct" not in item_answer or item_answer["correct"] is None:
                    return "Test was not created - correctness' answer is required", 400                
                
        name = data["name"]
        numQuestions = data["numQuestions"]
        minLevel = data["minLevel"]
        profiles = data["profiles"]
        skills = data["techSkills"]
        questions = data["questions"]

        # print("validation: ", country, isinstance(postId, int), size, (size in sizes), offer, (offer<=0))
        # 412  el caso que los valores no estén entre lo esperado
        # if(not isinstance(country, int) or size not in sizes or not isinstance(offer, int) or offer<=0): 
        #     return "parameter(s) not valid {} {} {}".format(postId, size, offer), 412

        try:
            num = int(minLevel)
            if(num<1 or num>5):
                return "Test was not created - minimum level is not valid", 412
        except ValueError:
            return "Test was not created - minimum level is not valid", 412

        try:
            num = int(numQuestions)
            if(num<0 or num>50):
                return "Test was not created - number of questions is not valid", 412
        except ValueError:
            return "Test was not created - number of questions is not valid", 412

        # return "Testing {}".format(filename), 404

        new_test = Test(name=name, numQuestions=numQuestions, minLevel=minLevel) #, profiles=profiles, techSkills=techSkills 
        #print()
        #print("init: ", new_test)

        for item in profiles:
            new_profile = Profile(profile=item["profile"], testId=new_test.id)
            new_test.profiles.append(new_profile)
            #print("  profile: ", new_profile)    
        #print("")

        for item in skills:
            new_tech_skill = TechnicalSkill(skill=item["skill"], testId=new_test.id)
            new_test.techSkills.append(new_tech_skill)
            #print("  tech_skills: ", new_tech_skill)    
        #print("")

        for item in questions:
            new_question = Question(question=item["question"], level=item["level"], url=item["url"], testId=new_test.id)
            for item_answer in item["answers"]:
                new_answer = Answer(answer=item_answer["answer"], correct=item_answer["correct"], questionId=new_question.id) #questionIdId=item_tech["id"]
                new_question.answers.append(new_answer)
                #print("    answer: ", new_answer)
            new_test.questions.append(new_question)
            #print("  question: ", new_question)    
        #print("")
        #print("done: ", new_test)
        db.session.add(new_test)
        db.session.commit()

        test_created = Test.query.filter(Test.name == name).filter(Test.minLevel==minLevel).order_by(Test.createdAt.desc()).first()
        return test_schema.dump(test_created), 201
