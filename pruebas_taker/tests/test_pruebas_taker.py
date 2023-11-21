import json
from app import app
#from model import db, Prueba
from faker import Faker
from unittest import TestCase
from unittest.mock import patch

class TestPruebasTaker(TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.fake = Faker()
     
        self.token = "mangocat"
        self.headers_token = {'Content-Type': 'application/json'} # , "Authorization": "Bearer {}".format(self.token)
        
        self.endpoint_health = '/tests-taker/ping'
        self.endpoint_init_400_candidatoId = '/tests-taker/init/id/1'
        self.endpoint_next_400_candidatoId = '/tests-taker/next/id/1'
        self.endpoint_done_400_candidatoId = '/tests-taker/done/id/1'
        self.endpoint_init_400_pruebaId = '/tests-taker/init/1/id'
        self.endpoint_next_400_pruebaId = '/tests-taker/next/1/id'
        self.endpoint_done_400_pruebaId = '/tests-taker/done/1/id'
        self.endpoint_init_200 = '/tests-taker/init/1/4'
        self.endpoint_next_200 = '/tests-taker/next/1/4'
        self.endpoint_done_200 = '/tests-taker/done/1/4'

        profiles = []
        techSkills = []
        questions = []
        numQuestions = self.fake.random_int(5, 5)

        for x in range(3):
            profiles.append({"id": self.fake.random_int(10, 49), "profile": self.fake.job()})
        for x in range(3):
            techSkills.append({"id": self.fake.random_int(50, 99), "skill": self.fake.sentence(2)})
        for x in range(numQuestions*2):
            answers = []
            for y in range(5):
                answers.append({"id": self.fake.random_int(1000, 9999), "answer": self.fake.sentence(2), "correct": False})
            answers[0]["correct"] = True
            question = {
                "id": self.fake.random_int(100, 199), 
                "level": self.fake.random_int(1, 5), 
                "question": self.fake.sentence(3), 
                "answers": answers
            }
            questions.append(question)

        self.prueba = {
            "id": self.fake.random_int(100, 199),
            "name": self.fake.bs(),
            "numQuestions": numQuestions,
            "minLevel": self.fake.random_int(1, 5),
            "profiles": profiles,
            "techSkills": techSkills, 
            "questions": questions, 
            "createdAt": "2023-11-12T22:57:59.819296"
        }

        self.candidato = {
            "id": self.fake.random_int(1000, 1999), 
            "name": self.fake.first_name(), 
            "lastName": self.fake.last_name(),
            "username": self.fake.email(),
            "softSkills": [{"skill": self.fake.word()}, {"skill": self.fake.word()}],
            "technicalSkills": [{"skill": self.fake.job()}, {"skill": self.fake.job()}],
            "createdAt": "2023-11-12T23:26:05.081973"
        }

        self.prueba_candidato = {
            "id": self.fake.random_int(100, 999),
            "idcandidate": self.candidato['id'],
            "idtest": self.prueba['id'],
            "maxdatepresent": "2023-11-28",
            "testestatus": "ASIGNADA",
            "createdAt": "2023-11-18T22:29:16.157050"
        }

        self.next_question = {
            'totalQuestions': self.fake.random_int(5, 10), 
            'numQuestion': self.fake.random_int(1, 5), 
            'questionId': self.fake.random_int(100, 199),
            'answerId': self.fake.random_int(200, 299),
        }

    def test_health_check(self):
        req_health = self.client.get(self.endpoint_health, headers={'Content-Type': 'application/json'})
        self.assertEqual(req_health.status_code, 200)

    @patch('view.setupCache')
    def test_init_test_400_candidatoId(self, mock_setup_cache):
        mock_setup_cache.return_value = ''
        req_get = self.client.post(self.endpoint_init_400_candidatoId, headers=self.headers_token)
        self.assertEqual(req_get.status_code, 400)

    @patch('view.setupCache')
    def test_init_test_400_testId(self, mock_setup_cache):
        mock_setup_cache.return_value = ''
        req_get = self.client.post(self.endpoint_init_400_pruebaId, headers=self.headers_token)
        self.assertEqual(req_get.status_code, 400)

    @patch('view.setupCache')
    @patch('view.getCandidato')
    def test_init_test_404_candidato_not_found(self, mock_candidato, mock_setup_cache):
        mock_setup_cache.return_value = ''
        mock_candidato.return_value = {'msg': 'candidato was not found by mango', 'status_code': 404}
        req = self.client.post(self.endpoint_init_200, headers=self.headers_token)
        #print("test-404: ", json.loads(req.get_data())) 
        self.assertEqual(req.status_code, 404)

    @patch('view.setupCache')
    @patch('view.getCandidato')
    @patch('view.getPrueba')
    def test_init_test_404_test_not_found(self, mock_prueba, mock_candidato, mock_setup_cache):
        mock_setup_cache.return_value = ''
        mock_candidato.return_value = {'msg': self.candidato, 'status_code': 200}
        mock_prueba.return_value = {'msg': 'prueba was not found by mango', 'status_code': 404}
        req = self.client.post(self.endpoint_init_200, headers=self.headers_token)
        #print("test-404: ", json.loads(req.get_data()))
        self.assertEqual(req.status_code, 404)

    @patch('view.setupCache')
    @patch('view.getCandidato')
    @patch('view.getPrueba')
    @patch('view.getPruebaCandidato')    
    def test_init_test_404_candidato_test_not_associated(self, mock_prueba_candidato, mock_prueba, mock_candidato, mock_setup_cache):
        mock_setup_cache.return_value = ''
        mock_candidato.return_value = {'msg': self.candidato, 'status_code': 200}
        mock_prueba.return_value = {'msg': self.prueba, 'status_code': 200}
        mock_prueba_candidato.return_value = {'msg': 'prueba is not associated to candidato by mango', 'status_code': 404}
        req = self.client.post(self.endpoint_init_200, headers=self.headers_token)
        #print("test-404: ", json.loads(req.get_data()))
        self.assertEqual(req.status_code, 404)

    @patch('view.setupCache')
    @patch('view.getCache')
    def test_next_test_412_last_question(self, mock_get_cache, mock_setup_cache):
        mock_setup_cache.return_value = ''
        mock_get_cache.return_value = None
        self.next_question = {
            'numQuestion': self.prueba["numQuestions"], 
            'totalQuestions': self.prueba["numQuestions"], 
            'questionId': self.prueba["questions"][1]["id"],
            'answerId': self.prueba["questions"][1]["answers"][0]["id"]
        }
        req_get = self.client.post(self.endpoint_next_200, headers=self.headers_token, data=json.dumps(self.next_question))
        self.assertEqual(req_get.status_code, 404)


    @patch('view.setupCache')
    @patch('view.getCandidato')
    @patch('view.getPrueba')
    @patch('view.getPruebaCandidato')
    @patch('view.deleteCache')
    @patch('view.setCache')
    @patch('view.getCache')
    def test_init_test_200(self, mock_get_cache, mock_set_cache, mock_delete_cache, mock_prueba_candidato, mock_prueba, mock_candidato, mock_setup_cache):
        mock_setup_cache.return_value = ''
        mock_candidato.return_value = {'msg': self.candidato, 'status_code': 200}
        mock_prueba.return_value = {'msg': self.prueba, 'status_code': 200}
        mock_prueba_candidato.return_value = {'msg': self.prueba_candidato, 'status_code': 200}
        mock_delete_cache.return_value = ''
        mock_set_cache.return_value = ''
        mock_get_cache.return_value = {
            'pruebaId': self.prueba['id'],
            'candidatoId': self.candidato['id'],
            "totalQuestions": self.prueba['numQuestions'],
            "numQuestion": 1, 
            "answersOK": 0, 
            "prueba": self.prueba,
            "candidato": self.candidato,
        }
        req = self.client.post(self.endpoint_init_200, headers=self.headers_token)
        # print()
        # print(json.loads(req.get_data()))
        self.assertEqual(req.status_code, 200)

    @patch('view.setupCache')
    def test_next_test_400_candidatoId(self, mock_setup_cache):
        mock_setup_cache.return_value = ''
        req_get = self.client.post(self.endpoint_next_400_candidatoId, headers=self.headers_token)
        self.assertEqual(req_get.status_code, 400)

    @patch('view.setupCache')
    def test_next_test_400_testId(self, mock_setup_cache):
        mock_setup_cache.return_value = ''
        req_get = self.client.post(self.endpoint_next_400_pruebaId, headers=self.headers_token)
        self.assertEqual(req_get.status_code, 400)

    @patch('view.setupCache')
    def test_next_test_400_totalQuestions(self, mock_setup_cache):
        mock_setup_cache.return_value = ''
        self.next_question["totalQuestions"] = None
        req_get = self.client.post(self.endpoint_next_200, headers=self.headers_token, data=json.dumps(self.next_question))
        self.assertEqual(req_get.status_code, 400)

    @patch('view.setupCache')
    def test_next_test_400_numQuestion(self, mock_setup_cache):
        mock_setup_cache.return_value = ''
        self.next_question["numQuestion"] = None
        req_get = self.client.post(self.endpoint_next_200, headers=self.headers_token, data=json.dumps(self.next_question))
        self.assertEqual(req_get.status_code, 400)

    @patch('view.setupCache')
    def test_next_test_400_questionId(self, mock_setup_cache):
        mock_setup_cache.return_value = ''
        self.next_question["questionId"] = None
        req_get = self.client.post(self.endpoint_next_200, headers=self.headers_token, data=json.dumps(self.next_question))
        self.assertEqual(req_get.status_code, 400)        

    @patch('view.setupCache')
    def test_next_test_400_answerId(self, mock_setup_cache):
        mock_setup_cache.return_value = ''
        self.next_question["answerId"] = None
        req_get = self.client.post(self.endpoint_next_200, headers=self.headers_token, data=json.dumps(self.next_question))
        self.assertEqual(req_get.status_code, 400)

    @patch('view.setupCache')
    @patch('view.getCache')
    def test_next_test_404_candidateId_testId(self, mock_get_cache, mock_setup_cache):
        mock_setup_cache.return_value = ''
        mock_get_cache.return_value = None
        req_get = self.client.post(self.endpoint_next_200, headers=self.headers_token, data=json.dumps(self.next_question))
        self.assertEqual(req_get.status_code, 404)

    @patch('view.setupCache')
    @patch('view.getCache')
    @patch('view.setCache')
    def test_next_test_200(self, mock_set_cache, mock_get_cache, mock_setup_cache):
        mock_setup_cache.return_value = ''
        mock_get_cache.return_value = {
            'pruebaId': self.prueba['id'],
            'candidatoId': self.candidato['id'],
            "totalQuestions": self.prueba['numQuestions'],
            "numQuestion": 1, 
            "answersOK": 0, 
            "prueba": self.prueba,
            "candidato": self.candidato,
        }
        mock_set_cache.return_value = {}

        self.next_question = {
            'numQuestion': 1, 
            'totalQuestions': self.prueba["numQuestions"], 
            'questionId': self.prueba["questions"][1]["id"],
            'answerId': self.prueba["questions"][1]["answers"][0]["id"]
        }
        req = self.client.post(self.endpoint_next_200, headers=self.headers_token, data=json.dumps(self.next_question))
        # print()
        # print(json.loads(req.get_data()))
        self.assertEqual(req.status_code, 200)

    @patch('view.setupCache')
    def test_done_test_400_candidatoId(self, mock_setup_cache):
        mock_setup_cache.return_value = ''
        req_get = self.client.post(self.endpoint_done_400_candidatoId, headers=self.headers_token)
        self.assertEqual(req_get.status_code, 400)

    @patch('view.setupCache')
    def test_done_test_400_testId(self, mock_setup_cache):
        mock_setup_cache.return_value = ''
        req_get = self.client.post(self.endpoint_done_400_pruebaId, headers=self.headers_token)
        self.assertEqual(req_get.status_code, 400)

    @patch('view.setupCache')
    def test_done_test_400_totalQuestions(self, mock_setup_cache):
        mock_setup_cache.return_value = ''
        self.next_question["totalQuestions"] = None
        req_get = self.client.post(self.endpoint_done_200, headers=self.headers_token, data=json.dumps(self.next_question))
        self.assertEqual(req_get.status_code, 400)

    @patch('view.setupCache')
    def test_done_test_400_numQuestion(self, mock_setup_cache):
        mock_setup_cache.return_value = ''
        self.next_question["numQuestion"] = None
        req_get = self.client.post(self.endpoint_done_200, headers=self.headers_token, data=json.dumps(self.next_question))
        self.assertEqual(req_get.status_code, 400)

    @patch('view.setupCache')
    def test_done_test_400_questionId(self, mock_setup_cache):
        mock_setup_cache.return_value = ''
        self.next_question["questionId"] = None
        req_get = self.client.post(self.endpoint_done_200, headers=self.headers_token, data=json.dumps(self.next_question))
        self.assertEqual(req_get.status_code, 400)        

    @patch('view.setupCache')
    def test_done_test_400_answerId(self, mock_setup_cache):
        mock_setup_cache.return_value = ''
        self.next_question["answerId"] = None
        req_get = self.client.post(self.endpoint_done_200, headers=self.headers_token, data=json.dumps(self.next_question))
        self.assertEqual(req_get.status_code, 400)

    @patch('view.setupCache')
    @patch('view.getCache')
    def test_done_test_404_candidateId_testId(self, mock_get_cache, mock_setup_cache):
        mock_setup_cache.return_value = ''
        mock_get_cache.return_value = None
        req_get = self.client.post(self.endpoint_done_200, headers=self.headers_token, data=json.dumps(self.next_question))
        self.assertEqual(req_get.status_code, 404)

    @patch('view.setupCache')
    @patch('view.getCache')
    def test_done_test_412_last_question(self, mock_get_cache, mock_setup_cache):
        mock_setup_cache.return_value = ''
        mock_get_cache.return_value = None
        self.next_question = {
            'numQuestion': self.prueba["numQuestions"]-1, 
            'totalQuestions': self.prueba["numQuestions"], 
            'questionId': self.prueba["questions"][1]["id"],
            'answerId': self.prueba["questions"][1]["answers"][0]["id"]
        }
        req_get = self.client.post(self.endpoint_done_200, headers=self.headers_token, data=json.dumps(self.next_question))
        self.assertEqual(req_get.status_code, 404)

    @patch('view.setupCache')
    @patch('view.getCache')
    @patch('view.setCache')
    @patch('view.updatePruebaCandidato')    
    def test_done_test_400_update_result(self, mock_prueba_candidato, mock_set_cache, mock_get_cache, mock_setup_cache):
        mock_setup_cache.return_value = ''
        mock_get_cache.return_value = {
            'pruebaId': self.prueba['id'],
            'candidatoId': self.candidato['id'],
            "totalQuestions": self.prueba['numQuestions'],
            "numQuestion": 1, 
            "answersOK": 0, 
            "prueba": self.prueba,
            "candidato": self.candidato,
        }
        mock_set_cache.return_value = {}
        mock_prueba_candidato.return_value = {'msg': 'parameters required by mango', 'status_code': 400}
        self.next_question = {
            'numQuestion': self.prueba["numQuestions"], 
            'totalQuestions': self.prueba["numQuestions"], 
            'questionId': self.prueba["questions"][1]["id"],
            'answerId': self.prueba["questions"][1]["answers"][0]["id"]
        }
        req = self.client.post(self.endpoint_done_200, headers=self.headers_token, data=json.dumps(self.next_question))
        self.assertEqual(req.status_code, 400)

    @patch('view.setupCache')
    @patch('view.getCache')
    @patch('view.setCache')
    @patch('view.updatePruebaCandidato')
    def test_done_test_200(self, mock_candidate_test, mock_set_cache, mock_get_cache, mock_setup_cache):
        mock_setup_cache.return_value = ''
        mock_get_cache.return_value = {
            'pruebaId': self.prueba['id'],
            'candidatoId': self.candidato['id'],
            "totalQuestions": self.prueba['numQuestions'],
            "numQuestion": 1, 
            "answersOK": 0, 
            "prueba": self.prueba,
            "candidato": self.candidato,
        }
        mock_set_cache.return_value = {}
        candidateTest = {
            'pruebaId': self.prueba['id'], 
            'candidatoId': self.candidato['id'],
            'result': 3.69,
        }
        mock_candidate_test.return_value = {'msg': candidateTest, 'status_code': 200}
        self.next_question = {
            'numQuestion': self.prueba["numQuestions"], 
            'totalQuestions': self.prueba["numQuestions"], 
            'questionId': self.prueba["questions"][1]["id"],
            'answerId': self.prueba["questions"][1]["answers"][0]["id"]
        }
        req = self.client.post(self.endpoint_done_200, headers=self.headers_token, data=json.dumps(self.next_question))
        # print()
        # print(json.loads(req.get_data()))
        self.assertEqual(req.status_code, 200)

    @patch('view.setupCache')
    @patch('view.getCandidato')
    @patch('view.getPrueba')
    @patch('view.getPruebaCandidato')
    @patch('view.deleteCache')
    @patch('view.setCache')
    @patch('view.getCache')
    @patch('view.updatePruebaCandidato')    
    def test_all_test_200_result5(self, mock_candidate_test, mock_get_cache, mock_set_cache, mock_delete_cache, mock_prueba_candidato, mock_prueba, mock_candidato, mock_setup_cache):
        mock_setup_cache.return_value = ''
        mock_candidato.return_value = {'msg': self.candidato, 'status_code': 200}
        mock_prueba.return_value = {'msg': self.prueba, 'status_code': 200}
        mock_prueba_candidato.return_value = {'msg': self.prueba_candidato, 'status_code': 200}
        mock_delete_cache.return_value = ''
        mock_set_cache.return_value = ''
        mock_get_cache.return_value = {
            'pruebaId': self.prueba['id'],
            'candidatoId': self.candidato['id'],
            "totalQuestions": self.prueba['numQuestions'],
            "numQuestion": 1, 
            "answersOK": 0, 
            "prueba": self.prueba,
            "candidato": self.candidato,
        }
        req = self.client.post(self.endpoint_init_200, headers=self.headers_token)
        # print()
        # print(json.loads(req.get_data()))
        self.assertEqual(req.status_code, 200)

        numQuestions = self.prueba['numQuestions']
        for x in range(1, numQuestions+1):
            mock_setup_cache.return_value = ''
            mock_get_cache.return_value = {
                'pruebaId': self.prueba['id'],
                'candidatoId': self.candidato['id'],
                "totalQuestions": self.prueba['numQuestions'],
                "numQuestion": x, 
                "answersOK": x-1,
                "prueba": self.prueba,
                "candidato": self.candidato,
            }
            mock_set_cache.return_value = {}
            self.next_question = {
                'numQuestion': x, 
                'totalQuestions': self.prueba["numQuestions"], 
                'questionId': self.prueba["questions"][x-1]["id"],
                'answerId': self.prueba["questions"][x-1]["answers"][0]["id"]
            }
            if(x == numQuestions):
                candidateTest = {
                    'pruebaId': self.prueba['id'], 
                    'candidatoId': self.candidato['id'],
                    'result': 3.69,
                }
                mock_candidate_test.return_value = {'msg': candidateTest, 'status_code': 200}
                req = self.client.post(self.endpoint_done_200, headers=self.headers_token, data=json.dumps(self.next_question))            
                resp = json.loads(req.get_data())
                #print("result: ", resp['result'])
                self.assertEqual(5.0, resp['result'])
            else: 
                req = self.client.post(self.endpoint_next_200, headers=self.headers_token, data=json.dumps(self.next_question))
            self.assertEqual(req.status_code, 200)

