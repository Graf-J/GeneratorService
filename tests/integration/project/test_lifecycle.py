import asyncio
import os
import shutil
import unittest

from fastapi.testclient import TestClient

from main import app


class TestProjectLifecycle(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app, backend_options={'loop_factory': asyncio.new_event_loop})

        # Setup Project Folder
        dir_path = os.path.join(os.getcwd(), 'projects')
        os.mkdir(dir_path)

    def tearDown(self):
        # Delete Folder
        dir_path = os.path.join(os.getcwd(), 'projects')
        shutil.rmtree(dir_path)

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
