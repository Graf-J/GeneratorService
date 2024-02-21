import asyncio
import os
import shutil
import unittest

from fastapi.testclient import TestClient

from main import app


class TestProjectGetAll(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app, backend_options={'loop_factory': asyncio.new_event_loop})

        # Setup Project Folder
        dir_path = os.path.join(os.getcwd(), 'projects')
        os.mkdir(dir_path)

        # Create one Project
        response = self.client.post('/api/v1/projects', json={'name': 'ValidName'})
        self.project = response.json()

    def tearDown(self):
        # Delete Folder
        dir_path = os.path.join(os.getcwd(), 'projects')
        shutil.rmtree(dir_path)

    def test(self):
        # Act
        response = self.client.get('/api/v1/projects')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0].get('id'), self.project.get('id'))
        self.assertEqual(response.json()[0].get('name'), self.project.get('name'))
