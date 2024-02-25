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

        # Create Vertices
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/vertices", json={
            'name': 'Person',
            'position_x': 10,
            'position_y': 20,
            'radius': 30,
            'properties': []
        })
        self.person_vertex = response.json()
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/vertices", json={
            'name': 'Hobby',
            'position_x': 40,
            'position_y': 50,
            'radius': 60,
            'properties': []
        })
        self.hobby_vertex = response.json()

        # Create Edges
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/edges", json={
            'name': 'performs',
            'properties': [],
            'multi_edge': False,
            'source_vertex_id': self.person_vertex.get('id'),
            'target_vertex_id': self.hobby_vertex.get('id')
        })
        self.performs_edge = response.json()
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/edges", json={
            'name': 'likes',
            'properties': [],
            'multi_edge': True,
            'source_vertex_id': self.person_vertex.get('id'),
            'target_vertex_id': self.person_vertex.get('id')
        })
        self.likes_edge = response.json()

    def tearDown(self):
        # Delete Folder
        dir_path = os.path.join(os.getcwd(), 'projects')
        shutil.rmtree(dir_path)

    def test_with_wrong_project_id(self):
        # Act
        response = self.client.get("/api/v1/projects/invalid-id/graph")

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'Project not found')

    def test_with_valid_project_id(self):
        # Act
        response = self.client.get(f"/api/v1/projects/{self.project.get('id')}/graph")

        # Assert
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.json().get('vertices')), 2)
        self.assertEqual(len(response.json().get('edges')), 2)

        self.assertEqual(len(response.json().get('vertices')[0].get('out_edges')), 2)
        self.assertEqual(len(response.json().get('vertices')[0].get('in_edges')), 1)

        self.assertEqual(len(response.json().get('vertices')[1].get('out_edges')), 0)
        self.assertEqual(len(response.json().get('vertices')[1].get('in_edges')), 1)
