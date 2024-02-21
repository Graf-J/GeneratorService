import asyncio
import os
import shutil
import unittest

from fastapi.testclient import TestClient

from main import app


class TestVertexLifecycle(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app, backend_options={'loop_factory': asyncio.new_event_loop})

        # Setup Project Folder
        dir_path = os.path.join(os.getcwd(), 'projects')
        os.mkdir(dir_path)

        # Setup Project
        project_res = self.client.post('/api/v1/projects', json={'name': 'Test-Project'})
        self.project = project_res.json()

    def tearDown(self):
        # Delete Folder
        dir_path = os.path.join(os.getcwd(), 'projects')
        shutil.rmtree(dir_path)

    def test_lifecycle(self):
        # Get Empty Vertices List
        response = self.client.get(f"/api/v1/projects/{self.project.get('id')}/vertices")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

        # Create Two Vertices
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/vertices", json={
            'name': 'FirstVertex',
            'position_x': 10,
            'position_y': 20,
            'radius': 30,
            'properties': []
        })
        first_vertex = response.json()
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/vertices", json={
            'name': 'SecondVertex',
            'position_x': 50,
            'position_y': 60,
            'radius': 70,
            'properties': []
        })
        second_vertex = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(second_vertex.get('name'), 'SecondVertex')

        # Connect FirstVertex recursively to itself
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/edges", json={
            'name': 'recursive_edge',
            'properties': [],
            'source_vertex_id': first_vertex.get('id'),
            'target_vertex_id': first_vertex.get('id')
        })
        recursive_edge = response.json()
        self.assertEqual(response.status_code, 200)

        # Connect FirstVertex to SecondVertex
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/edges", json={
            'name': 'ordinary_edge',
            'properties': [],
            'source_vertex_id': first_vertex.get('id'),
            'target_vertex_id': second_vertex.get('id')
        })
        ordinary_edge = response.json()
        self.assertEqual(response.status_code, 200)

        # Get all Vertices
        response = self.client.get(f"/api/v1/projects/{self.project.get('id')}/vertices")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(len(response.json()[0].get('out_edges')), 2)
        self.assertEqual(len(response.json()[0].get('in_edges')), 1)

        # Update FirstVertex
        response = self.client.put(
            f"/api/v1/projects/{self.project.get('id')}/vertices/{first_vertex.get('id')}",
            json={
                'name': 'UpdatedVertex',
                'position_x': 1,
                'position_y': 2,
                'radius': 3,
                'properties': [
                    {
                        'key': 'name',
                        'required': False,
                        'datatype': 'ID'
                    }
                ]
            })
        updated_vertex = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_vertex.get('id'), first_vertex.get('id'))

        # Get UpdatedVertex
        response = self.client.get(f"/api/v1/projects/{self.project.get('id')}/vertices/{updated_vertex.get('id')}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('id'), updated_vertex.get('id'))
        self.assertEqual(response.json().get('name'), 'UpdatedVertex')
        self.assertEqual(response.json().get('position_x'), 1)
        self.assertEqual(response.json().get('position_y'), 2)
        self.assertEqual(response.json().get('radius'), 3)
        self.assertIsInstance(response.json().get('properties'), list)
        self.assertEqual(len(response.json().get('properties')), 1)
        self.assertEqual(len(response.json().get('out_edges')), 2)
        self.assertEqual(response.json().get('out_edges')[0].get('id'), recursive_edge.get('id'))
        self.assertEqual(response.json().get('out_edges')[0].get('name'), 'recursive_edge')
        self.assertEqual(response.json().get('out_edges')[1].get('id'), ordinary_edge.get('id'))
        self.assertEqual(response.json().get('out_edges')[1].get('name'), 'ordinary_edge')
        self.assertEqual(len(response.json().get('in_edges')), 1)
        self.assertEqual(response.json().get('in_edges')[0].get('id'), recursive_edge.get('id'))
        self.assertEqual(response.json().get('in_edges')[0].get('name'), 'recursive_edge')

        # Delete SecondVertex
        response = self.client.delete(f"/api/v1/projects/{self.project.get('id')}/vertices/{second_vertex.get('id')}")
        self.assertEqual(response.status_code, 200)

        # Get all Vertices
        response = self.client.get(f"/api/v1/projects/{self.project.get('id')}/vertices")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

        # Get UpdatedVertex
        response = self.client.get(f"/api/v1/projects/{self.project.get('id')}/vertices/{updated_vertex.get('id')}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json().get('out_edges')), 1)
        self.assertEqual(response.json().get('out_edges')[0].get('id'), recursive_edge.get('id'))
        self.assertEqual(response.json().get('out_edges')[0].get('name'), 'recursive_edge')
        self.assertEqual(len(response.json().get('in_edges')), 1)
        self.assertEqual(response.json().get('in_edges')[0].get('id'), recursive_edge.get('id'))
        self.assertEqual(response.json().get('in_edges')[0].get('name'), 'recursive_edge')
