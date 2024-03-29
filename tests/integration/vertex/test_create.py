import asyncio
import os
import shutil
import unittest

from fastapi.testclient import TestClient

from main import app


class TestVertexCreate(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app, backend_options={'loop_factory': asyncio.new_event_loop})

        # Setup Project Folder
        dir_path = os.path.join(os.getcwd(), 'projects')
        os.mkdir(dir_path)

        # Setup Project
        project_res = self.client.post('/api/v1/projects', json={'name': 'Test-Project'})
        self.project = project_res.json()

        # Create Vertex
        vertex_res = self.client.post(f"/api/v1/projects/{self.project.get('id')}/vertices", json={
            'name': 'TestVertex',
            'position_x': 10,
            'position_y': 20,
            'properties': [
                {
                    'key': 'test_prop',
                    'required': True,
                    'datatype': 'String'
                }
            ]
        })
        self.vertex = vertex_res.json()

    def tearDown(self):
        # Delete Folder
        dir_path = os.path.join(os.getcwd(), 'projects')
        shutil.rmtree(dir_path)

    def test_with_wrong_project_id(self):
        # Act
        response = self.client.post(f"/api/v1/projects/invalid-id/vertices", json={
            'name': 'NewVertex',
            'position_x': 10,
            'position_y': 20,
            'properties': []
        })

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'Project not found')

    def test_with_missing_name(self):
        # Act
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/vertices", json={
            'position_x': 10,
            'position_y': 20,
            'properties': []
        })

        # Assert
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'Field required')

    def test_with_empty_name(self):
        # Act
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/vertices", json={
            'name': '',
            'position_x': 10,
            'position_y': 20,
            'properties': []
        })

        # Assert
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'String should have at least 1 character')

    def test_with_name_with_starting_number(self):
        # Act
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/vertices", json={
            'name': '1-New-Vertex',
            'position_x': 10,
            'position_y': 20,
            'properties': []
        })

        # Assert
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'),
                         'Value error, Name must start with a letter or underscore, followed by letters, numbers, or underscores.')

    def test_with_name_with_minus(self):
        # Act
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/vertices", json={
            'name': 'New-Vertex',
            'position_x': 10,
            'position_y': 20,
            'properties': []
        })

        # Assert
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'),
                         'Value error, Name must start with a letter or underscore, followed by letters, numbers, or underscores.')

    def test_with_missing_position_x(self):
        # Act
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/vertices", json={
            'name': 'NewVertex',
            'position_y': 20,
            'properties': []
        })

        # Assert
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'Field required')

    def test_with_missing_position_y(self):
        # Act
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/vertices", json={
            'name': 'NewVertex',
            'position_x': 10,
            'properties': []
        })

        # Assert
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'Field required')

    def test_with_missing_properties(self):
        # Act
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/vertices", json={
            'name': 'NewVertex',
            'position_x': 10,
            'position_y': 20,
        })

        # Assert
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'Field required')

    def test_with_property_name_with_starting_number(self):
        # Act
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/vertices", json={
            'name': 'NewVertex',
            'position_x': 10,
            'position_y': 20,
            'properties': [
                {
                    'key': '1name',
                    'required': True,
                    'datatype': 'String'
                }
            ]
        })

        # Assert
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'),
                         'Value error, Key must start with a letter or underscore, followed by letters, numbers, or underscores.')

    def test_with_property_name_with_minus(self):
        # Act
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/vertices", json={
            'name': 'NewVertex',
            'position_x': 10,
            'position_y': 20,
            'properties': [
                {
                    'key': 'new-name',
                    'required': True,
                    'datatype': 'String'
                }
            ]
        })

        # Assert
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'),
                         'Value error, Key must start with a letter or underscore, followed by letters, numbers, or underscores.')

    def test_with_duplicate_name(self):
        # Act
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/vertices", json={
            'name': 'TestVertex',
            'position_x': 10,
            'position_y': 20,
            'properties': [
                {
                    'key': 'name',
                    'required': True,
                    'datatype': 'String'
                }
            ]
        })

        # Assert
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'), "Vertex with Name 'TestVertex' already exists")

    def test_with_valid_vertex(self):
        # Act
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/vertices", json={
            'name': 'NewVertex',
            'position_x': 10,
            'position_y': 20,
            'properties': [
                {
                    'key': 'name',
                    'required': True,
                    'datatype': 'String'
                }
            ]
        })

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json().get('id'), str)
        self.assertEqual(response.json().get('name'), 'NewVertex')
        self.assertEqual(response.json().get('position_x'), 10)
        self.assertEqual(response.json().get('position_y'), 20)
        self.assertIsInstance(response.json().get('properties'), list)
        self.assertEqual(len(response.json().get('properties')), 1)
        self.assertEqual(response.json().get('properties')[0].get('key'), 'name')
        self.assertEqual(response.json().get('properties')[0].get('required'), True)
        self.assertEqual(response.json().get('properties')[0].get('datatype'), 'String')
