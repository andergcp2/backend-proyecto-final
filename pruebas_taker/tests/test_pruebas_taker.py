import json
from app import app
#from model import db, Prueba
from faker import Faker
from unittest import TestCase
from unittest.mock import patch

class TestPruebasTaker(TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.data_factory = Faker()
     
        self.token = "mangocat"
        self.headers_token = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        
        self.endpoint_health = '/tests-taker/ping'
        self.endpoint_init_400_candidatoId = '/tests-taker/init/id/1'
        self.endpoint_next_400_candidatoId = '/tests-taker/next/id/1'
        self.endpoint_done_400_candidatoId = '/tests-taker/done/id/1'
        self.endpoint_init_400_pruebaId = '/tests-taker/init/1/id'
        self.endpoint_next_400_pruebaId = '/tests-taker/next/1/id'
        self.endpoint_done_400_pruebaId = '/tests-taker/done/1/id'

        self.endpoint_init_404 = '/tests-taker/init/1/4'
        self.endpoint_init_200 = '/tests-taker/init/1/4'
        self.endpoint_next_404 = '/tests-taker/next/1/4'
        self.endpoint_next_200 = '/tests-taker/next/1/4'
        self.endpoint_done_404 = '/tests-taker/done/1/4'
        self.endpoint_done_200 = '/tests-taker/done/1/4'
        #self.endpoint_init_200 = '/pruebas/init/9/45'
        #self.endpoint_init_200 = '/pruebas-orquestador/{}/{}'.format(str(self.id_prueba), str(self.id_prueba))

        # self.post_resp_ok = {'msg': {"id": self.postId, "routeId": self.routeId, "userId": self.userId}, 'status_code': 200}
        # self.route_resp_ok = {'msg': {"id": self.routeId, "bagCost": self.bagCost}, 'status_code': 200}
        # self.offer_resp_ok = {'msg': {"id": self.offerId, "userId": self.id, "createdAt": datetime.now().isoformat()}, 'status_code': 201}

        self.candidato_200 = {
            "softSkills": [{"skill": "Teamwork"}, {"skill": "Communication"}],
            "technicalSkills": [{"skill": "Back-End Development"}, {"skill": "Cloud Computing"}],
            "id": 1, 
            "name": "Alexandra", 
            "lastName": "Suarez", 
            "username": "alexaSz1",
            "createdAt": "2023-11-12T23:26:05.081973"            
        }

        self.prueba_200 = {
            "profiles": [{"id": 8, "profile": "Forest/woodland manager"}, {"id": 9, "profile": "Curator"}, {"id": 10, "profile": "Conservation officer, nature"}],
            "techSkills": [{"id": 8, "skill": "field"}, {"id": 9, "skill": "economic"}, {"id": 10, "skill": "gas"}],
            "questions": [
                {
                    "id": 28, "question": "Build city capital.", "level": 2,
                    "answers": [
                        {"id": 82, "answer": "Capital place.", "correct": False}, 
                        {"id": 83, "answer": "Admit.", "correct": False}, 
                        {"id": 84, "answer": "Field marriage.", "correct": True}
                    ]
                },
                {
                    "id": 29, "question": "Expect wish.", "level": 1,
                    "answers": [
                        {"id": 85, "answer": "Deep.", "correct": False},
                        {"id": 86, "answer": "Language.", "correct": False},
                        {"id": 87, "answer": "Project.", "correct": True}
                    ]
                },
                {
                    "id": 30, "question": "Manage something book.", "level": 2,
                    "answers": [
                        {"id": 88, "answer": "Our control.", "correct": False},
                        {"id": 89, "answer": "They wind.", "correct": False},
                        {"id": 90, "answer": "Red.", "correct": True}
                    ]
                },
                {
                    "id": 31, "question": "Hour color home.", "level": 4,
                    "answers": [
                        {"id": 91, "answer": "President word.", "correct": False},
                        {"id": 92, "answer": "Chair.", "correct": False},
                        {"id": 93, "answer": "Chance tell.", "correct": True}
                    ]
                },
                {
                    "id": 32, "question": "Science you.", "level": 1, "answers": [
                        {"id": 94, "answer": "Human.", "correct": False},
                        {"id": 95, "answer": "Whatever.", "correct": False},
                        {"id": 96, "answer": "Approach.", "correct": True}
                    ]
                },
                {
                    "id": 33, "question": "Fear door chair.", "level": 1,
                    "answers": [
                        {"id": 97, "answer": "Security.", "correct": False},
                        {"id": 98, "answer": "Say.", "correct": False},
                        {"id": 99, "answer": "Occur machine.", "correct": True}
                    ]
                },
                {
                    "id": 34, "question": "Character future board.", "level": 4,
                    "answers": [
                        {"id": 100, "answer": "Performance.", "correct": False},
                        {"id": 101, "answer": "Ever.", "correct": False},
                        {"id": 102, "answer": "To value.", "correct": True}
                    ]
                },
                {
                    "id": 35, "question": "Art.", "level": 3,
                    "answers": [
                        {"id": 103, "answer": "Political late.", "correct": False},
                        {"id": 104, "answer": "Can yes.", "correct": False},
                        {"id": 105, "answer": "Such.", "correct": True}
                    ]
                },
                {
                    "id": 36, "question": "Their energy environmental.", "level": 5,
                    "answers": [
                        {"id": 106, "answer": "Force.", "correct": False},
                        {"id": 107, "answer": "System camera.", "correct": False},
                        {"id": 108, "answer": "Speak.", "correct": True}
                    ]
                }
            ],
            "id": 4,
            "name": "Electrical engineer implement rich e-markets",
            "numQuestions": 43,
            "minLevel": 5,
            "createdAt": "2023-11-12T22:57:59.819296"
        }

        self.prueba_candidato_200 = {
            "id": 6,
            "idcandidate": 1,
            "idtest": 4,
            "maxdatepresent": "2023-11-28",
            "testestatus": "ASIGNADA",
            "createdAt": "2023-11-18T22:29:16.157050"
        }        

    def test_health_check(self):
        req_health = self.client.get(self.endpoint_health, headers={'Content-Type': 'application/json'})
        self.assertEqual(req_health.status_code, 200)

    def test_init_test_400_candidatoId(self):
        req_get = self.client.post(self.endpoint_init_400_candidatoId, headers=self.headers_token)
        self.assertEqual(req_get.status_code, 400)

    def test_init_test_400_testId(self):
        req_get = self.client.post(self.endpoint_init_400_pruebaId, headers=self.headers_token)
        self.assertEqual(req_get.status_code, 400)

    @patch('view.getCandidato')
    def test_init_test_404_candidato_not_found(self, mock_candidato):
        mock_candidato.return_value = {'msg': 'candidato was not found by mango', 'status_code': 404}
        req = self.client.post(self.endpoint_init_404, headers=self.headers_token)
        #print("test-404: ", json.loads(req.get_data())) 
        self.assertEqual(req.status_code, 404)

    @patch('view.getCandidato')
    @patch('view.getPrueba')
    def test_init_test_404_test_not_found(self, mock_prueba, mock_candidato):
        mock_candidato.return_value = {'msg': self.candidato_200, 'status_code': 200}
        mock_prueba.return_value = {'msg': 'prueba was not found by mango', 'status_code': 404}
        req = self.client.post(self.endpoint_init_404, headers=self.headers_token)
        #print("test-404: ", json.loads(req.get_data()))
        self.assertEqual(req.status_code, 404)

    @patch('view.getCandidato')
    @patch('view.getPrueba')
    @patch('view.getPruebaCandidato')    
    def test_init_test_404_candidato_test_not_associated(self, mock_prueba_candidato, mock_prueba, mock_candidato):
        mock_candidato.return_value = {'msg': self.candidato_200, 'status_code': 200}
        mock_prueba.return_value = {'msg': self.prueba_200, 'status_code': 200}
        mock_prueba_candidato.return_value = {'msg': 'prueba is not associated to candidato by mango', 'status_code': 404}
        req = self.client.post(self.endpoint_init_404, headers=self.headers_token)
        #print("test-404: ", json.loads(req.get_data()))
        self.assertEqual(req.status_code, 404)

    @patch('view.getCandidato')
    @patch('view.getPrueba')
    @patch('view.getPruebaCandidato')
    @patch('view.deleteCache')
    @patch('view.setCache')
    @patch('view.getCache')
    def test_init_test_200(self, mock_get_cache, mock_set_cache, mock_delete_cache, mock_prueba_candidato, mock_prueba, mock_candidato):
        mock_candidato.return_value = {'msg': self.candidato_200, 'status_code': 200}
        mock_prueba.return_value = {'msg': self.prueba_200, 'status_code': 200}
        mock_prueba_candidato.return_value = {'msg': self.prueba_candidato_200, 'status_code': 200}
        mock_delete_cache.return_value = ''
        mock_set_cache.return_value = ''
        mock_get_cache.return_value = {}
        req = self.client.post(self.endpoint_init_200, headers=self.headers_token)
        # print("test-200: ", json.loads(req.get_data()))
        self.assertEqual(req.status_code, 200)

    def test_next_test_400_candidatoId(self):
        req_get = self.client.post(self.endpoint_next_400_candidatoId, headers=self.headers_token)
        self.assertEqual(req_get.status_code, 400)

    def test_next_test_400_testId(self):
        req_get = self.client.post(self.endpoint_next_400_pruebaId, headers=self.headers_token)
        self.assertEqual(req_get.status_code, 400)

    @patch('view.getCache')
    def test_next_test_200(self, mock_get_cache):
        mock_get_cache.return_value = {}
        req = self.client.post(self.endpoint_next_200, headers=self.headers_token)
        # print("test-200: ", json.loads(req.get_data()))
        self.assertEqual(req.status_code, 200)

    def test_done_test_400_candidatoId(self):
        req_get = self.client.post(self.endpoint_done_400_candidatoId, headers=self.headers_token)
        self.assertEqual(req_get.status_code, 400)

    def test_done_test_400_testId(self):
        req_get = self.client.post(self.endpoint_done_400_pruebaId, headers=self.headers_token)
        self.assertEqual(req_get.status_code, 400)

    @patch('view.getCache')
    @patch('view.updatePruebaCandidato')
    def test_done_test_404(self, mock_prueba_candidato, mock_get_cache):
        mock_get_cache.return_value = {}
        mock_prueba_candidato.return_value = {'msg': 'prueba was not updated by mango', 'status_code': 404}
        req = self.client.post(self.endpoint_done_404, headers=self.headers_token)
        # print("test-200: ", json.loads(req.get_data()))
        self.assertEqual(req.status_code, 404)

    @patch('view.getCache')
    @patch('view.updatePruebaCandidato')
    def test_done_test_200(self, mock_prueba_candidato, mock_get_cache):
        mock_get_cache.return_value = {}
        mock_prueba_candidato.return_value = {'msg': 'prueba updated by mango', 'status_code': 200}
        req = self.client.post(self.endpoint_done_200, headers=self.headers_token)
        # print("test-200: ", json.loads(req.get_data()))
        self.assertEqual(req.status_code, 200)

    # def test_init_test_404(self):
    #     req_get = self.client.post(self.endpoint_init_404, headers=self.headers_token)
    #     print(req_get.get_data())
    #     self.assertEqual(req_get.status_code, 404)

    # def test_init_test_200(self):
    #     req_get = self.client.post(self.endpoint_init_200, headers=self.headers_token)
    #     resp_get = json.loads(req_get.get_data())
    #     print("")
    #     print(resp_get)
    #     self.assertEqual(req_get.status_code, 200)

    #     req_get = self.client.post(self.endpoint_next_200, headers=self.headers_token)
    #     resp_get = json.loads(req_get.get_data())
    #     print("")
    #     print(resp_get)
    #     self.assertEqual(req_get.status_code, 200)

    #     req_get = self.client.post(self.endpoint_next_200, headers=self.headers_token)
    #     resp_get = json.loads(req_get.get_data())
    #     print("")
    #     print(resp_get)
    #     self.assertEqual(req_get.status_code, 200)
