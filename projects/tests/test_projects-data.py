import json
from app import app
from model import db, Project, Profile, SkillProfile, TestProfile
from faker import Faker
from unittest import TestCase
from unittest.mock import patch

class TestProjectsData(TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.fake = Faker()

    def test_create_projects(self):
        id = 0
        num = 369
        numProjects = 3
        numProfiles = 3
        numSkills = 2
        numTests = 2
        # proyId = 1

        for x1 in range(numProjects):
            new_project = Project(name=self.fake.bs(), type=self.fake.android_platform_token(), leader=self.fake.name(), 
            role=self.fake.job(), phone=self.fake.phone_number(), email=self.fake.company_email(), countryId=self.fake.country_code(), 
            cityId=self.fake.random_int(1, 99999), address=self.fake.street_address() +" "+ self.fake.street_name(), 
            companyId=self.fake.random_int(1, 999))

            for x2 in range(numProfiles):
                new_profile = Profile(name=self.fake.job(), professional=self.fake.job(), projectId=new_project.id)
                for x3 in range(numSkills):
                    new_profile.softskills.append(SkillProfile(skillId=self.fake.random_int(100, 999), profileId=new_profile.id)) 
                for x4 in range(numSkills):
                    new_profile.techskills.append(SkillProfile(skillId=self.fake.random_int(100, 999), profileId=new_profile.id)) 
                for x5 in range(numTests):
                    new_profile.tests.append(TestProfile(testId=self.fake.random_int(100, 999), profileId=new_profile.id)) 
                new_project.profiles.append(new_profile)

            db.session.add(new_project)
            db.session.commit()
            # Project.query.filter(Project.companyId == company).filter(Project.name==name).filter(Project.leader==leader).order_by(Project.createdAt.desc()).first()
            #print("project> ", project)

            # if(proyId==45): proyId=37
            # else: proyId=proyId+1

        self.assertEqual(num, 369)
