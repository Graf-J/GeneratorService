import os
import shutil
import unittest

from fastapi.testclient import TestClient

from main import app


class TestProject(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

        dir_path = os.path.join(os.getcwd(), 'projects')
        os.mkdir(dir_path)

    def tearDown(self):
        dir_path = os.path.join(os.getcwd(), 'projects')
        shutil.rmtree(dir_path)

    def test_get_with_wrong_id(self):
        response = self.client.get(f'/api/v1/projects/invalid-id')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'Project not found')

    def test_create_with_missing_name(self):
        response = self.client.post('/api/v1/projects', json={})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'Field required')

    def test_create_with_empty_name(self):
        response = self.client.post('/api/v1/projects', json={'name': ''})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'String should have at least 1 character')

    def test_create_with_underscore_in_name(self):
        response = self.client.post('/api/v1/projects', json={'name': 'hello_world'})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'),
                         'Value error, Filenames should not contain underscores, spaces, dots, or special characters.')

    def test_create_with_comma_in_name(self):
        response = self.client.post('/api/v1/projects', json={'name': 'Hello,World'})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'),
                         'Value error, Invalid characters in the filename.')

    def test_delete_with_wrong_id(self):
        response = self.client.delete(f'/api/v1/projects/invalid-id')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'Project not found')

    def test_lifecycle(self):
        # Get Empty Projects List
        response = self.client.get('/api/v1/projects')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

        # Create Two Projects
        self.client.post('/api/v1/projects', json={'name': 'Project-1'})
        response = self.client.post('api/v1/projects', json={'name': 'Project-2'})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json().get('id'), str)
        self.assertEqual(response.json().get('name'), 'Project-2')

        # Get both Projects
        response = self.client.get('/api/v1/projects')
        id_1 = response.json()[0].get('id')
        id_2 = response.json()[1].get('id')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertIsInstance(id_1, str)
        self.assertIsInstance(id_2, str)
        self.assertEqual(response.json()[0].get('name'), 'Project-1')
        self.assertEqual(response.json()[1].get('name'), 'Project-2')

        # Get first Project
        response = self.client.get(f'/api/v1/projects/{id_1}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('id'), id_1)
        self.assertEqual(response.json().get('name'), 'Project-1')

        # Delete one Project
        response = self.client.delete(f'/api/v1/projects/{id_1}')
        self.assertEqual(response.status_code, 200)

        # Get remaining Project
        response = self.client.get('/api/v1/projects')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0].get('id'), id_2)
        self.assertEqual(response.json()[0].get('name'), 'Project-2')

        # Delete second Project
        response = self.client.delete(f'/api/v1/projects/{id_2}')
        self.assertEqual(response.status_code, 200)

        # Get Empty Projects List
        response = self.client.get('/api/v1/projects')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
