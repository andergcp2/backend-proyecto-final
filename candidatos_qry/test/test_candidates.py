import json
from unittest import TestCase
from unittest.mock import MagicMock, patch
from app import app
from faker import Faker


class TestCompany(TestCase):
    """Class for test service"""

    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()
        self.endpoint_create = '/candidates'
        self.endpoint_health = '/candidates/ping'

    def test_health(self):
        """Test for health check ping"""
        req_health = self.client.get(self.endpoint_health, headers={'Content-Type': 'application/json'})
        json.loads(req_health.get_data())
        self.assertEqual(req_health.status_code, 200)

    def test_create_candidate_400_request_empty(self):
        """Test for empty candidate"""
        new_company = {}
        resp_create = self.client.post(self.endpoint_create, headers={'Content-Type': 'application/json'}, data=json.dumps(new_company))
        error_code = json.loads(resp_create.get_data()).get('errorCode')
        self.assertEqual(error_code, 'CO01')
        self.assertEqual(resp_create.status_code, 400)

    @patch('vistas.requests.post')
    def test_create_candidate_201_creation_success(self, mock_post):
        """Test for create candidate"""
        new_candidate = {
            "name": "Jhon",
            "lastName": "Doe",
            "idType": "CC",
            "identification": "1234567",
            "email": "jhon_doe@mail.com",
            "phone": "1234567890",
            "country": "Colombia",
            "city": "Bogota",
            "address": "Calle 123",
            "profession": "Ingeniero de sistemas",
            "softSkills": ["Trabajo en equipo", "Comunicacion"],
            "technicalSkills": [],
            "username": "jhonDoe1234",
            "password": "pass1234",
            "passwordConfirmation": "pass1234"
        }

        mock_response = MagicMock()
        mock_post.status_code = 200
        mock_post.return_value.text = '{\"statusCode\": 200,\"body\": \"{\\"message\\":\\"User signed up successfully\\"}\"}'
        mock_response.return_value = mock_post
        resp_create = self.client.post(self.endpoint_create, headers={'Content-Type': 'application/json'}, data=json.dumps(new_candidate))
        print(resp_create.get_data())
        self.assertEqual(resp_create.status_code, 201)

    def test_create_candidate_400_invalid_request(self):
        new_company = {
            "name": "Jhon",
            "lastName": "Doe",
            "idType": "CC123456",
            "identification": "1234567",
            "email": "jhon_doe@mail.com",
            "phone": "1234567890",
            "country": "Colombia",
            "city": "Bogota",
            "address": "Calle 123",
            "profession": "Ingeniero de sistemas",
            "softSkills": ["Trabajo en equipo", "Comunicacion"],
            "technicalSkills": [],
            "username": "jhonDoe1234",
            "password": "pass1234",
            "passwordConfirmation": "pass12345"
        }
        resp_create = self.client.post(self.endpoint_create, headers={'Content-Type': 'application/json'}, data=json.dumps(new_company))
        error_code = json.loads(resp_create.get_data()).get('errorCode')
        self.assertEqual(error_code, 'CO02')
        self.assertEqual(resp_create.status_code, 400)

    def test_create_candidate_400_password_not_match(self):
        new_company = {
            "name": "Jhon",
            "lastName": "Doe",
            "idType": "CC",
            "identification": "1234567",
            "email": "jhon_doe@mail.com",
            "phone": "1234567890",
            "country": "Colombia",
            "city": "Bogota",
            "address": "Calle 123",
            "profession": "Ingeniero de sistemas",
            "softSkills": ["Trabajo en equipo", "Comunicacion"],
            "technicalSkills": [],
            "username": "jhonDoe1234",
            "password": "pass1234",
            "passwordConfirmation": "pass12345"
        }
        resp_create = self.client.post(self.endpoint_create, headers={'Content-Type': 'application/json'}, data=json.dumps(new_company))
        error_code = json.loads(resp_create.get_data()).get('errorCode')
        self.assertEqual(error_code, 'CO03')
        self.assertEqual(resp_create.status_code, 400)

    @patch('vistas.requests.post')
    def test_create_candidate_400_cognito_client_error(self, mock_post):
        new_company = {
            "name": "Jhon",
            "lastName": "Doe",
            "idType": "CC",
            "identification": "1234567",
            "email": "jhon_doe@mail.com",
            "phone": "1234567890",
            "country": "Colombia",
            "city": "Bogota",
            "address": "Calle 123",
            "profession": "Ingeniero de sistemas",
            "softSkills": ["Trabajo en equipo", "Comunicacion"],
            "technicalSkills": [],
            "username": "jhonDoe1234",
            "password": "pass1234",
            "passwordConfirmation": "pass1234"
        }
        mock_response = MagicMock()
        mock_post.status_code = 200
        mock_post.return_value.text = "{\"errorType\":\"Error\",\"errorMessage\":\"Sign-upfailed\",\"trace\":[\"Error:Sign-upfailed\",\"atRuntime.exports.handler(/var/task/index.js:27:15)\",\"atprocessTicksAndRejections(internal/process/task_queues.js:95:5)\"]}"
        mock_response.return_value = mock_post
        resp_create = self.client.post(self.endpoint_create, headers={'Content-Type': 'application/json'}, data=json.dumps(new_company))
        error_code = json.loads(resp_create.get_data()).get('errorCode')
        self.assertEqual(error_code, 'CO04')
        self.assertEqual(resp_create.status_code, 400)


    def test_get_all_companies_200(self):
        resp_get = self.client.get(self.endpoint_create, headers={'Content-Type': 'application/json'})
        print(resp_get.get_data())
        self.assertEqual(resp_get.status_code, 200)
