import asyncio
import os
import shutil
import unittest

from fastapi.testclient import TestClient

from main import app


class TestProjectGetOne(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app, backend_options={'loop_factory': asyncio.new_event_loop})

        # Setup Project Folder
        dir_path = os.path.join(os.getcwd(), 'projects')
        os.mkdir(dir_path)

        # Create one Project
        response = self.client.post('/api/v1/projects', json={'name': 'Test'})
        self.project = response.json()

    def tearDown(self):
        # Delete Folder
        dir_path = os.path.join(os.getcwd(), 'projects')
        shutil.rmtree(dir_path)

    def test_with_wrong_id(self):
        # Act
        response = self.client.get(f'/api/v1/projects/invalid-id')

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'Project not found')

    def test_with_existing_id(self):
        # Act
        response = self.client.get(f"/api/v1/projects/{self.project.get('id')}")

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('id'), self.project.get('id'))
        self.assertEqual(response.json().get('name'), self.project.get('name'))
