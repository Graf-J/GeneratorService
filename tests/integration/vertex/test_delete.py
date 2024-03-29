import asyncio
import os
import shutil
import unittest

from fastapi.testclient import TestClient

from main import app


class TestVertexDelete(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app, backend_options={'loop_factory': asyncio.new_event_loop})

        # Setup Project Folder
        dir_path = os.path.join(os.getcwd(), 'projects')
        os.mkdir(dir_path)

        # Setup Project
        project_res = self.client.post('/api/v1/projects', json={'name': 'Test-Project'})
        self.project = project_res.json()

        # Create Vertices
        first_vertex_res = self.client.post(f"/api/v1/projects/{self.project.get('id')}/vertices", json={
            'name': 'FirstVertex',
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
        self.first_vertex = first_vertex_res.json()
        second_vertex_res = self.client.post(f"/api/v1/projects/{self.project.get('id')}/vertices", json={
            'name': 'SecondVertex',
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
        self.second_vertex = second_vertex_res.json()

        # Create Edges
        first_edge_res = self.client.post(f"/api/v1/projects/{self.project.get('id')}/edges", json={
            'name': 'recursive',
            'properties': [],
            'multi_edge': True,
            'source_vertex_id': self.first_vertex.get('id'),
            'target_vertex_id': self.first_vertex.get('id')
        })
        self.first_edge = first_edge_res.json()
        second_edge_res = self.client.post(f"/api/v1/projects/{self.project.get('id')}/edges", json={
            'name': 'ordinary',
            'properties': [],
            'multi_edge': False,
            'source_vertex_id': self.first_vertex.get('id'),
            'target_vertex_id': self.second_vertex.get('id')
        })
        self.second_edge = second_edge_res.json()

    def tearDown(self):
        # Delete Folder
        dir_path = os.path.join(os.getcwd(), 'projects')
        shutil.rmtree(dir_path)

    def test_with_wrong_project_id(self):
        # Act
        response = self.client.delete(f"/api/v1/projects/invalid-id/vertices/{self.first_vertex.get('id')}")

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'Project not found')

    def test_with_wrong_vertex_id(self):
        # Act
        response = self.client.delete(f"/api/v1/projects/{self.project.get('id')}/vertices/invalid-id")

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json().get('detail')[0].get('msg'), "Vertex with Id 'invalid-id' not found")

    def test_with_valid_project_id_and_valid_vertex_id_scenario_1(self):
        # Act
        response = self.client.delete(
            f"/api/v1/projects/{self.project.get('id')}/vertices/{self.first_vertex.get('id')}")

        # Assert
        self.assertEqual(response.status_code, 200)

        vertices = self.client.get(f"/api/v1/projects/{self.project.get('id')}/vertices")
        self.assertEqual(len(vertices.json()), 1)

        self.assertEqual(len(vertices.json()[0].get('out_edges')), 0)
        self.assertEqual(len(vertices.json()[0].get('in_edges')), 0)

        edges = self.client.get(f"/api/v1/projects/{self.project.get('id')}/edges")
        self.assertEqual(len(edges.json()), 0)

    def test_with_valid_project_id_and_valid_vertex_id_scenario_2(self):
        # Act
        response = self.client.delete(
            f"/api/v1/projects/{self.project.get('id')}/vertices/{self.second_vertex.get('id')}")

        # Assert
        self.assertEqual(response.status_code, 200)

        vertices = self.client.get(f"/api/v1/projects/{self.project.get('id')}/vertices")
        self.assertEqual(len(vertices.json()), 1)

        self.assertEqual(len(vertices.json()[0].get('out_edges')), 1)
        self.assertEqual(len(vertices.json()[0].get('in_edges')), 1)

        edges = self.client.get(f"/api/v1/projects/{self.project.get('id')}/edges")
        self.assertEqual(len(edges.json()), 1)
