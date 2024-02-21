import asyncio
import os
import shutil
import unittest

from fastapi.testclient import TestClient

from main import app


class TestProjectDelete(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app, backend_options={'loop_factory': asyncio.new_event_loop})

        # Setup Project Folder
        dir_path = os.path.join(os.getcwd(), 'projects')
        os.mkdir(dir_path)

    def tearDown(self):
        # Delete Folder
        dir_path = os.path.join(os.getcwd(), 'projects')
        shutil.rmtree(dir_path)

    def test_with_existing_id(self):
        # Arrange
        response = self.client.post('/api/v1/projects', json={'name': 'Test'})
        project_id = response.json().get('id')

        # Act
        response = self.client.delete(f'api/v1/projects/{project_id}')

        # Assert
        self.assertEqual(response.status_code, 200)

    def test_with_wrong_id(self):
        # Act
        response = self.client.delete(f'/api/v1/projects/invalid-id')

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'Project not found')
