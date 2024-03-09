import asyncio
import os
import shutil
import unittest

from fastapi.testclient import TestClient

from main import app


class TestVertexGetAll(unittest.TestCase):
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
        response = self.client.get("/api/v1/projects/invalid-id/vertices")

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'Project not found')

    def test_with_valid_project_id(self):
        # Act
        response = self.client.get(f"/api/v1/projects/{self.project.get('id')}/vertices")

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0].get('id'), self.vertex.get('id'))
