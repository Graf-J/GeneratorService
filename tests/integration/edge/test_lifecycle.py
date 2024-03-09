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

    def tearDown(self):
        # Delete Folder
        dir_path = os.path.join(os.getcwd(), 'projects')
        shutil.rmtree(dir_path)

    def test_lifecycle(self):
        # Get Empty Edges List
        response = self.client.get(f"/api/v1/projects/{self.project.get('id')}/vertices")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

        # Create Two Vertices
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/vertices", json={
            'name': 'FirstVertex',
            'position_x': 10,
            'position_y': 20,
            'properties': []
        })
        person_vertex = response.json()
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/vertices", json={
            'name': 'SecondVertex',
            'position_x': 50,
            'position_y': 60,
            'properties': []
        })
        hobby_vertex = response.json()

        # Create one Edge between Person and Hobby
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/edges", json={
            'name': 'performs',
            'properties': [],
            'multi_edge': False,
            'source_vertex_id': person_vertex.get('id'),
            'target_vertex_id': hobby_vertex.get('id')
        })
        performs_edge = response.json()
        self.assertEqual(response.status_code, 200)

        # Create one recursive Edge for Person
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/edges", json={
            'name': 'likes',
            'properties': [],
            'multi_edge': False,
            'source_vertex_id': person_vertex.get('id'),
            'target_vertex_id': person_vertex.get('id')
        })
        likes_edge = response.json()

        # Get both Edges
        response = self.client.get(f"/api/v1/projects/{self.project.get('id')}/edges")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

        # Check Edges of Vertices
        response = self.client.get(f"/api/v1/projects/{self.project.get('id')}/vertices")
        self.assertEqual(len(response.json()[0].get('out_edges')), 2)
        self.assertEqual(response.json()[0].get('out_edges')[0].get('id'), performs_edge.get('id'))
        self.assertEqual(response.json()[0].get('out_edges')[0].get('name'), performs_edge.get('name'))
        self.assertEqual(response.json()[0].get('out_edges')[1].get('id'), likes_edge.get('id'))
        self.assertEqual(response.json()[0].get('out_edges')[1].get('name'), likes_edge.get('name'))

        self.assertEqual(len(response.json()[0].get('in_edges')), 1)
        self.assertEqual(response.json()[0].get('in_edges')[0].get('id'), likes_edge.get('id'))
        self.assertEqual(response.json()[0].get('in_edges')[0].get('name'), likes_edge.get('name'))

        self.assertEqual(len(response.json()[1].get('out_edges')), 0)

        self.assertEqual(len(response.json()[1].get('in_edges')), 1)
        self.assertEqual(response.json()[1].get('in_edges')[0].get('id'), performs_edge.get('id'))
        self.assertEqual(response.json()[1].get('in_edges')[0].get('name'), performs_edge.get('name'))

        # Update one Edge
        response = self.client.put(
            f"/api/v1/projects/{self.project.get('id')}/edges/{performs_edge.get('id')}",
            json={
                'name': 'gets_played',
                'properties': [],
                'multi_edge': False,
                'source_vertex_id': hobby_vertex.get('id'),
                'target_vertex_id': person_vertex.get('id')
            })
        self.assertEqual(response.status_code, 200)

        # Get updated Edge
        response = self.client.get(f"/api/v1/projects/{self.project.get('id')}/edges/{performs_edge.get('id')}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('id'), performs_edge.get('id'))
        self.assertEqual(response.json().get('name'), 'gets_played')
        self.assertEqual(response.json().get('multi_edge'), False)
        self.assertEqual(response.json().get('source_vertex_id'), hobby_vertex.get('id'))
        self.assertEqual(response.json().get('target_vertex_id'), person_vertex.get('id'))

        # Delete one Edge
        response = self.client.delete(f"/api/v1/projects/{self.project.get('id')}/edges/{performs_edge.get('id')}")
        self.assertEqual(response.status_code, 200)

        # Get all Edges
        response = self.client.get(f"/api/v1/projects/{self.project.get('id')}/edges")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0].get('id'), likes_edge.get('id'))

        # Verify the Vertices
        response = self.client.get(f"/api/v1/projects/{self.project.get('id')}/vertices")
        self.assertEqual(len(response.json()), 2)

        self.assertEqual(len(response.json()[0].get('out_edges')), 1)
        self.assertEqual(response.json()[0].get('out_edges')[0].get('id'), likes_edge.get('id'))

        self.assertEqual(len(response.json()[0].get('in_edges')), 1)
        self.assertEqual(response.json()[0].get('in_edges')[0].get('id'), likes_edge.get('id'))

        self.assertEqual(len(response.json()[1].get('out_edges')), 0)

        self.assertEqual(len(response.json()[1].get('in_edges')), 0)
