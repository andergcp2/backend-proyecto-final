import json, requests
from flask import request, current_app
from flask_restful import Resource
from model import db, Project, Profile, SkillProfile, TestProfile, ProjectSchema, ProfileSchema, SkillProfileSchema, TestProfileSchema
# from datetime import datetime

project_schema = ProjectSchema()
profile_schema = ProfileSchema()
skill_profile_schema = SkillProfileSchema()

class HealthCheck(Resource):
    def get(self):
        return "ok"

class Projects(Resource):

    def post(self):
        # resp = validate_token(request.headers)
        # if(resp['status_code'] != 200):
        #     return resp['msg'], resp['status_code']

        name = type = company = leader = role = phone = email = country = city = address = None
        data = request.get_json()
        if "name" not in data or request.json["name"] is None:
            return "project's name is required", 400
        elif "type" not in data:
            return "project's type is required", 400
        elif "company" not in data:
            return "project's company is required", 400
        elif "leader" not in data:
            return "project's leader is required", 400
        elif "role" not in data:
            return "project's leader role is required", 400
        elif "phone" not in data:
            return "project's leader phone is required", 400
        elif "email" not in data:
            return "project's leader email is required", 400
        elif "country" not in data:
            return "project's country is required", 400
        elif "city" not in data:
            return "project's city is required", 400
        elif "address" not in data:
            return "project's  address is required", 400
        elif "profiles" not in data:
            return "project's profiles are required", 400

        name = request.json["name"]
        type = request.json["type"]
        company = request.json["company"]
        leader = request.json["leader"]
        role = request.json["role"]
        phone = request.json["phone"]
        email = request.json["email"]
        country = request.json["country"]
        city = request.json["city"]
        address = request.json["address"]
        profiles = request.json["profiles"]

        # print("validation: ", country, isinstance(postId, int), size, (size in sizes), offer, (offer<=0))
        # 412  el caso que los valores no estén entre lo esperado
        # if(not isinstance(country, int) or size not in sizes or not isinstance(offer, int) or offer<=0): 
        #     return "parameter(s) not valid {} {} {}".format(postId, size, offer), 412

        try:
            int(company)
        except ValueError:
            return "project's company is not valid: {}".format(company), 412

        try:
            int(city)
        except ValueError:
            return "project's city is not valid: {}".format(city), 412

        new_project = Project(name=name, type=type, leader=leader, role=role, phone=phone, email=email, 
        countryId=country, cityId=city, address=address, companyId=company) #createdAt=datetime.now()

        #print("init: ", new_project)
        for item in profiles:
            new_profile = Profile(name=item["name"], profession=item["profession"], projectId=new_project.id)
            for item_soft in item["softskills"]:
                new_skill = SkillProfile(skillId=item_soft["id"], profileId=new_profile.id)
                new_profile.softskills.append(new_skill) 
                #print("    softskill: ", new_skill)
            for item_tech in item["techskills"]:
                new_skill = SkillProfile(skillId=item_tech["id"], profileId=new_profile.id)
                new_profile.techskills.append(new_skill)
                #print("    techskill: ", new_skill)
            for item_test in item["tests"]:
                new_test = TestProfile(testId=item_tech["id"], profileId=new_profile.id)
                new_profile.tests.append(new_test)     
                #print("    testprof: ", new_test)        
            
            new_project.profiles.append(new_profile)
            #print("  profile: ", new_profile)    
        #print("")
        #print("done: ", new_project)
        
        db.session.add(new_project)
        db.session.commit()
        project_created = Project.query.filter(Project.companyId == company).filter(Project.name==name).filter(Project.leader==leader).order_by(Project.createdAt.desc()).first()
        
        #project_created = db.session.query(Project).filter(Project.companyId==company).filter(Project.name==name).filter(Project.leader==leader).order_by(Project.createdAt.desc()).first()
        #Profile, SkillProfile, TestProfile
        #.filter(Project.id==Profile.projectId)
        #.filter(SkillProfile.profileId==Profile.id).filter(TestProfile.profileId==Profile.id)
        return project_schema.dump(project_created), 201

    def get(self):
        # resp = validate_token(request.headers)
        # if(resp['status_code'] != 200):
        #     return resp['msg'], resp['status_code']
        projects = db.session.query(Project).select_from(Project).all()
        return [project_schema.dump(p) for p in Project.query.all()], 200

class GetCompanyProjects(Resource):

    def get(self, companyId):
        return [project_schema.dump(p) for p in Project.query.filter(Project.companyId == companyId).all()], 200

class GetProject(Resource):

    def get(self, projectId):
        return project_schema.dump(Project.query.get_or_404(projectId))
