import json, requests
from flask import request, current_app, jsonify
from flask_restful import Resource
from model import db, Project, Profile, SoftSkillProfile, TechSkillProfile, TestProfile, ProjectCandidate, CandidateEvaluation
from model import ProjectSchema, ProfileSchema, SoftSkillProfileSchema, TechSkillProfileSchema, TestProfileSchema, ProjectCandidateSchema, CandidateEvaluationSchema
# from datetime import datetime

project_schema = ProjectSchema()
profile_schema = ProfileSchema()
project_candidate_schema = ProjectCandidateSchema()
candidate_evaluation_schema = CandidateEvaluationSchema()

def getCandidato(endpoint, headers):
    return requestMicro("get", endpoint, headers, None)

def requestMicro(method, endpoint, headers, data):
    try:
        # if(method == 'get'):
        #     resp = requests.put(endpoint, headers = headers, data=json.dumps(data))
        resp = requests.get(endpoint, headers = headers)

        if (resp.status_code==200):
            return {'msg': resp.json(), 'status_code': resp.status_code}
        return {'msg': resp.text, 'status_code': resp.status_code} 
    except Exception as ex:
        return {'msg': 'connection endpoint failed {} -> {}'.format(endpoint, ex), 'status_code': 500}


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
                new_skill = SoftSkillProfile(skillId=item_soft["id"], profileId=new_profile.id)
                new_profile.softskills.append(new_skill) 
                #print("    softskill: ", new_skill)
            for item_tech in item["techskills"]:
                new_skill = TechSkillProfile(skillId=item_tech["id"], profileId=new_profile.id)
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

    def get(self, id):
        if id is not None: 
            try:
                int(id)
            except ValueError:
                return "the project id is not a number", 412

        project = Project.query.filter(Project.id == id).first()
        if project is None:
            return "the project with the given id was not found", 404

        return project_schema.dump(project)

class SetCandidateProject(Resource):

    def post(self, projectId, candidatoId):
        headers = {"Content-Type":"application/json"} # , "Authorization": request.headers['Authorization']

        if projectId is not None: 
            try:
                int(projectId)
            except ValueError:
                return "project id is not a number", 400

        if candidatoId is not None: 
            try:
                int(candidatoId)
            except ValueError:
                return "candidato id is not a number", 400

        # 400 si alguno de los parametros no esta presente
        if projectId is None or candidatoId is None: 
            return "parameter(s) missing", 400

        project = Project.query.filter(Project.id == projectId).first()
        if project is None:
            return "the project with the given id was not found", 404

        endpoint = format(current_app.config['CANDIDATOS_QUERY']) +"/{}".format(candidatoId)
        #print ("candidato-url: ", endpoint)
        resp = getCandidato(endpoint, headers)
        if(resp['status_code'] != 200):
            # 404 - El candidato no existe
            return resp, resp['status_code'] # Response(resp['msg'], resp['status_code']) resp.headers.items()
        candidato = resp['msg']

        query = ProjectCandidate.query.filter(ProjectCandidate.projectId == projectId).filter(ProjectCandidate.candidateId==candidatoId).order_by(ProjectCandidate.createdAt.desc()).first()
        if(query is not None):
            return "the project with the given id is already associated to candidate", 412

        new_project_candidate = ProjectCandidate(projectId=projectId, candidateId=candidatoId) 
        db.session.add(new_project_candidate)
        db.session.commit()

        created = ProjectCandidate.query.filter(ProjectCandidate.projectId == projectId).filter(ProjectCandidate.candidateId==candidatoId).order_by(ProjectCandidate.createdAt.desc()).first()
        #print("created:", project_candidate_schema.dump(created))
        return project_candidate_schema.dump(created), 201


class GetCandidatesProject(Resource):

    def get(self, projectId):
        headers = {"Content-Type":"application/json"} # , "Authorization": request.headers['Authorization']

        if projectId is not None: 
            try:
                int(projectId)
            except ValueError:
                return "project id is not a number", 400

        # 400 si alguno de los parametros no esta presente
        if projectId is None: 
            return "parameter(s) missing", 400

        project = Project.query.filter(Project.id == projectId).first()
        if project is None:
            return "the project with the given id was not found", 404

        candidates = []
        query = ProjectCandidate.query.filter(ProjectCandidate.projectId == projectId).order_by(ProjectCandidate.createdAt.desc()).all()
        for candidate in query:
            endpoint = format(current_app.config['CANDIDATOS_QUERY']) +"/{}".format(candidate.candidateId)
            #print("req :", endpoint)
            resp = getCandidato(endpoint, headers)
            #print("resp:", resp)
            if(resp['status_code'] == 200):
                candidates.append(
                    {
                        'id': resp['msg']['id'], 
                        'name': resp['msg']['name'], 
                        'lastName': resp['msg']['lastName'], 
                        'email': resp['msg']['email'], 
                        'phone': resp['msg']['phone']
                    }
                )

        # return [project_candidate_schema.dump(pc) for pc in query]
        
        # return candidates, 200
        return [json.dumps(cand) for cand in candidates], 200
        # return json.dumps(candidates), 200

class GetCandidatesCompany(Resource):

    def get(self, companyId):
        headers = {"Content-Type":"application/json"} # , "Authorization": request.headers['Authorization']

        if companyId is not None: 
            try:
                int(companyId)
            except ValueError:
                return "company id is not a number", 400

        # 400 si alguno de los parametros no esta presente
        if companyId is None:
            return "parameter(s) missing", 400

        projects = Project.query.filter(Project.companyId == companyId).all()
        if projects is None:
            return "Projects with the given companyId was not found", 404
        
        #print(projects)
        projectsIds = []

        for project in projects:
            projectsIds.append(project.id)

        candidates = []
        query = ProjectCandidate.query.filter(ProjectCandidate.projectId.in_(projectsIds)).all()
        #print(query)
        for candidate in query:
            print(candidate.candidateId)

            evaluation = CandidateEvaluation.query.filter(CandidateEvaluation.candidateId == candidate.candidateId)\
                                                .filter(CandidateEvaluation.projectId == candidate.projectId).first()
            comments = score = None
            if evaluation:
                score = evaluation.score
                comments = evaluation.comments

            endpoint = current_app.config['CANDIDATOS_QUERY']+"/{}".format(candidate.candidateId)
            resp = getCandidato(endpoint, headers)
            #print(resp)
            if(resp['status_code'] == 200):
                candidates.append(
                    {
                        "companyId": int(companyId),
                        "id": candidate.candidateId,
                        "projectId": candidate.projectId,
                        "name": resp["msg"]["name"], 
                        "lastName": resp["msg"]["lastName"], 
                        "email": resp["msg"]["email"], 
                        "phone": resp["msg"]["phone"],
                        "score": score,
                        "comments": comments
                    }
                )

        return candidates, 200

class EvaluationCandidateProject(Resource):

    def post(self, projectId, candidatoId):
        headers = {"Content-Type":"application/json"} # , "Authorization": request.headers['Authorization']

        if projectId is not None: 
            try:
                int(projectId)
            except ValueError:
                return "project id is not a number", 400

        if candidatoId is not None: 
            try:
                int(candidatoId)
            except ValueError:
                return "candidato id is not a number", 400

        # 400 si alguno de los parametros no esta presente
        if projectId is None or candidatoId is None: 
            return "parameter(s) missing", 400

        score = comments = None
        data = request.get_json()
        if "score" not in data or request.json["score"] is None:
            return "evaluation score is required", 400
        elif "comments" not in data or request.json["comments"] is None:
            return "evaluation comments are required", 400

        score = request.json["score"]
        comments = request.json["comments"]

        try:
            int(score)
        except ValueError:
            return "evaluation score is not valid: {}".format(score), 412

        if(score<0 or score>5):
            return "evaluation score is not in a valid range: {}".format(score), 412

        project = Project.query.filter(Project.id == projectId).first()
        if project is None:
            return "the project with the given id was not found", 404

        queryPC = ProjectCandidate.query.filter(ProjectCandidate.projectId == projectId).filter(ProjectCandidate.candidateId==candidatoId).first()
        if(queryPC is None):
            return "the project with the given id is not associated to candidate", 412

        queryEval = CandidateEvaluation.query.filter(CandidateEvaluation.projectId == projectId).filter(CandidateEvaluation.candidateId==candidatoId).first() 
        if(queryEval is not None):
            return "the candidate with the given id is already evaluated for the project", 412

        new_evaluation = CandidateEvaluation(projectId=projectId, candidateId=candidatoId, score=score, comments=comments) 
        db.session.add(new_evaluation)
        db.session.commit()

        created = CandidateEvaluation.query.filter(CandidateEvaluation.projectId == projectId).filter(CandidateEvaluation.candidateId==candidatoId).order_by(CandidateEvaluation.createdAt.desc()).first()
        return candidate_evaluation_schema.dump(created), 201

    # def get(self, projectId, candidatoId):
    #     headers = {"Content-Type":"application/json"} # , "Authorization": request.headers['Authorization']