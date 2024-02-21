import asyncio
import os
import shutil
import unittest

from fastapi.testclient import TestClient

from main import app


class TestProjectCreate(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app, backend_options={'loop_factory': asyncio.new_event_loop})

        # Setup Project Folder
        dir_path = os.path.join(os.getcwd(), 'projects')
        os.mkdir(dir_path)

    def tearDown(self):
        # Delete Folder
        dir_path = os.path.join(os.getcwd(), 'projects')
        shutil.rmtree(dir_path)

    def test_create_with_missing_name(self):
        response = self.client.post('/api/v1/projects', json={})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'Field required')

    def test_with_empty_name(self):
        # Act
        response = self.client.post('/api/v1/projects', json={'name': ''})

        # Assert
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'String should have at least 1 character')

    def test_with_underscore_in_name(self):
        # Act
        response = self.client.post('/api/v1/projects', json={'name': 'hello_world'})

        # Assert
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'),
                         'Value error, Filenames should not contain underscores, spaces, dots, or special characters.')

    def test_with_comma_in_name(self):
        # Act
        response = self.client.post('/api/v1/projects', json={'name': 'Hello,World'})

        # Assert
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'),
                         'Value error, Invalid characters in the filename.')

    def test_with_duplicate_name(self):
        # Arrange
        self.client.post('/api/v1/projects', json={'name': 'Test'})

        # Act
        response = self.client.post('/api/v1/projects', json={'name': 'Test'})

        # Assert
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json().get('detail')[0].get('msg'), "Project 'Test' already exists")

    def test_with_valid_name(self):
        # Act
        response = self.client.post('/api/v1/projects', json={'name': 'ValidName'})

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json().get('id'), str)
        self.assertEqual(response.json().get('name'), 'ValidName')
