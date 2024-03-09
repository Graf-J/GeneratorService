import asyncio
import os
import shutil
import unittest

from fastapi.testclient import TestClient

from main import app


class TestEdgeCreate(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app, backend_options={'loop_factory': asyncio.new_event_loop})

        # Setup Project Folder
        dir_path = os.path.join(os.getcwd(), 'projects')
        os.mkdir(dir_path)

        # Setup Project
        response = self.client.post('/api/v1/projects', json={'name': 'Test-Project'})
        self.project = response.json()

        # Create Vertices
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/vertices", json={
            'name': 'Person',
            'position_x': 10,
            'position_y': 20,
            'properties': []
        })
        self.person_vertex = response.json()
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/vertices", json={
            'name': 'Hobby',
            'position_x': 40,
            'position_y': 50,
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
        response = self.client.delete(f"/api/v1/projects/invalid-id/edges/{self.performs_edge.get('id')}")

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'Project not found')

    def test_with_wrong_edge_id(self):
        # Act
        response = self.client.delete(f"/api/v1/projects/{self.project.get('id')}/edges/invalid-id")

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json().get('detail')[0].get('msg'), "Edge with Id 'invalid-id' not found")

    def test_delete_ordinary_edge(self):
        # Act
        response = self.client.delete(f"/api/v1/projects/{self.project.get('id')}/edges/{self.performs_edge.get('id')}")

        # Assert
        self.assertEqual(response.status_code, 200)

        vertices = self.client.get(f"api/v1/projects/{self.project.get('id')}/vertices")
        self.assertEqual(len(vertices.json()), 2)

        self.assertEqual(len(vertices.json()[0].get('out_edges')), 1)
        self.assertEqual(vertices.json()[0].get('out_edges')[0].get('id'), self.likes_edge.get('id'))
        self.assertEqual(vertices.json()[0].get('out_edges')[0].get('name'), self.likes_edge.get('name'))

        self.assertEqual(len(vertices.json()[0].get('in_edges')), 1)
        self.assertEqual(vertices.json()[0].get('in_edges')[0].get('id'), self.likes_edge.get('id'))
        self.assertEqual(vertices.json()[0].get('in_edges')[0].get('name'), self.likes_edge.get('name'))

        self.assertEqual(len(vertices.json()[1].get('out_edges')), 0)
        self.assertEqual(len(vertices.json()[1].get('in_edges')), 0)

    def test_delete_recursive_edge(self):
        # Act
        response = self.client.delete(f"/api/v1/projects/{self.project.get('id')}/edges/{self.performs_edge.get('id')}")

        # Assert
        self.assertEqual(response.status_code, 200)

        vertices = self.client.get(f"api/v1/projects/{self.project.get('id')}/vertices")
        self.assertEqual(len(vertices.json()), 2)

        self.assertEqual(len(vertices.json()[0].get('out_edges')), 1)
        self.assertEqual(vertices.json()[0].get('out_edges')[0].get('id'), self.likes_edge.get('id'))
        self.assertEqual(vertices.json()[0].get('out_edges')[0].get('name'), self.likes_edge.get('name'))

        self.assertEqual(len(vertices.json()[0].get('in_edges')), 1)
        self.assertEqual(vertices.json()[0].get('in_edges')[0].get('id'), self.likes_edge.get('id'))
        self.assertEqual(vertices.json()[0].get('in_edges')[0].get('name'), self.likes_edge.get('name'))

        self.assertEqual(len(vertices.json()[1].get('out_edges')), 0)
        self.assertEqual(len(vertices.json()[1].get('in_edges')), 0)
