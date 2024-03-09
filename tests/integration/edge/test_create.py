import asyncio
import os
import shutil
import unittest
import uuid

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
            'properties': [
                {
                    'key': 'createsOut',
                    'required': True,
                    'datatype': 'String'
                }
            ]
        })
        self.person_vertex = response.json()
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/vertices", json={
            'name': 'Hobby',
            'position_x': 40,
            'position_y': 50,
            'properties': [
                {
                    'key': 'checksIn',
                    'required': False,
                    'datatype': 'String'
                }
            ]
        })
        self.hobby_vertex = response.json()

        # Create Edge
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/edges", json={
            'name': 'performs',
            'properties': [],
            'multi_edge': True,
            'source_vertex_id': self.person_vertex.get('id'),
            'target_vertex_id': self.hobby_vertex.get('id')
        })
        self.performs_edge = response.json()

    def tearDown(self):
        # Delete Folder
        dir_path = os.path.join(os.getcwd(), 'projects')
        shutil.rmtree(dir_path)

    def test_with_wrong_project_id(self):
        # Act
        response = self.client.post('/api/v1/projects/invalid-id/edges', json={
            'name': 'likes',
            'properties': [],
            'multi_edge': True,
            'source_vertex_id': self.person_vertex.get('id'),
            'target_vertex_id': self.person_vertex.get('id')
        })

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'Project not found')

    def test_with_wrong_source_vertex_id(self):
        # Arrange
        wrong_id = str(uuid.uuid4())

        # Act
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/edges", json={
            'name': 'likes',
            'properties': [],
            'multi_edge': False,
            'source_vertex_id': wrong_id,
            'target_vertex_id': self.person_vertex.get('id')
        })

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json().get('detail')[0].get('msg'), f"Vertex with Id '{wrong_id}' not found")

    def test_with_wrong_target_vertex_id(self):
        # Arrange
        wrong_id = str(uuid.uuid4())

        # Act
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/edges", json={
            'name': 'likes',
            'properties': [],
            'multi_edge': False,
            'source_vertex_id': self.person_vertex.get('id'),
            'target_vertex_id': wrong_id
        })

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json().get('detail')[0].get('msg'), f"Vertex with Id '{wrong_id}' not found")

    def test_with_missing_name(self):
        # Act
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/edges", json={
            'properties': [],
            'source_vertex_id': self.person_vertex.get('id'),
            'target_vertex_id': self.person_vertex.get('id')
        })

        # Assert
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'Field required')

    def test_with_empty_name(self):
        # Act
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/edges", json={
            'name': '',
            'properties': [],
            'source_vertex_id': self.person_vertex.get('id'),
            'target_vertex_id': self.person_vertex.get('id')
        })

        # Assert
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'String should have at least 1 character')

    def test_with_name_with_starting_number(self):
        # Act
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/edges", json={
            'name': '1likes',
            'properties': [],
            'source_vertex_id': self.person_vertex.get('id'),
            'target_vertex_id': self.person_vertex.get('id')
        })

        # Assert
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'),
                         'Value error, Name must start with a letter or underscore, followed by letters, numbers, or underscores.')

    def test_with_name_with_minus(self):
        # Act
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/edges", json={
            'name': 'likes-name',
            'properties': [],
            'source_vertex_id': self.person_vertex.get('id'),
            'target_vertex_id': self.person_vertex.get('id')
        })

        # Assert
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'),
                         'Value error, Name must start with a letter or underscore, followed by letters, numbers, or underscores.')

    def test_with_missing_properties(self):
        # Act
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/edges", json={
            'name': 'likes',
            'source_vertex_id': self.person_vertex.get('id'),
            'target_vertex_id': self.person_vertex.get('id')
        })

        # Assert
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'Field required')

    def test_with_minus_in_property_name(self):
        # Act
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/edges", json={
            'name': 'likes',
            'properties': [
                {
                    'key': 'property-key',
                    'required': True,
                    'type': 'String'
                }
            ],
            'source_vertex_id': self.person_vertex.get('id'),
            'target_vertex_id': self.person_vertex.get('id')
        })

        # Assert
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'),
                         "Value error, Key must start with a letter or underscore, followed by letters, numbers, or underscores.")

    def test_with_missing_multi_edge(self):
        # Act
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/edges", json={
            'name': 'likes',
            'properties': [],
            'source_vertex_id': self.person_vertex.get('id'),
            'target_vertex_id': self.person_vertex.get('id')
        })

        # Assert
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'Field required')

    def test_with_missing_source_vertex_id(self):
        # Act
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/edges", json={
            'name': 'likes',
            'properties': [],
            'target_vertex_id': self.person_vertex.get('id')
        })

        # Assert
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'Field required')

    def test_with_missing_target_vertex_id(self):
        # Act
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/edges", json={
            'name': 'likes',
            'properties': [],
            'source_vertex_id': self.person_vertex.get('id')
        })

        # Assert
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'Field required')

    def test_with_recursive_edge_with_same_name(self):
        # Act
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/edges", json={
            'name': 'performs',
            'properties': [],
            'multi_edge': True,
            'source_vertex_id': self.person_vertex.get('id'),
            'target_vertex_id': self.person_vertex.get('id')
        })

        # Assume
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json().get('detail')[0].get('msg'),
                         "Source-Vertex already has an outgoing edge with name 'performs'")

    def test_with_recursive_edge_with_different_name(self):
        # Act
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/edges", json={
            'name': 'likes',
            'properties': [],
            'multi_edge': False,
            'source_vertex_id': self.person_vertex.get('id'),
            'target_vertex_id': self.person_vertex.get('id')
        })

        # Assume
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json().get('id'), str)
        self.assertEqual(response.json().get('name'), 'likes')
        self.assertEqual(len(response.json().get('properties')), 0)
        self.assertEqual(response.json().get('multi_edge'), False)
        self.assertEqual(response.json().get('source_vertex_id'), self.person_vertex.get('id'))
        self.assertEqual(response.json().get('target_vertex_id'), self.person_vertex.get('id'))

        person_vertex = self.client.get(
            f"/api/v1/projects/{self.project.get('id')}/vertices/{self.person_vertex.get('id')}")
        self.assertEqual(person_vertex.json().get('out_edges')[1].get('id'), response.json().get('id'))
        self.assertEqual(person_vertex.json().get('in_edges')[0].get('id'), response.json().get('id'))

    def test_with_ordinary_edge_with_same_name(self):
        # Act
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/edges", json={
            'name': 'performs',
            'properties': [],
            'multi_edge': False,
            'source_vertex_id': self.person_vertex.get('id'),
            'target_vertex_id': self.hobby_vertex.get('id')
        })

        # Assume
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json().get('detail')[0].get('msg'),
                         "Source-Vertex already has an outgoing edge with name 'performs'")

    def test_with_opposite_edge_with_same_name(self):
        # Act
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/edges", json={
            'name': 'performs',
            'properties': [],
            'multi_edge': True,
            'source_vertex_id': self.hobby_vertex.get('id'),
            'target_vertex_id': self.person_vertex.get('id')
        })

        # Assume
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json().get('id'), str)
        self.assertEqual(response.json().get('name'), 'performs')
        self.assertEqual(len(response.json().get('properties')), 0)
        self.assertEqual(response.json().get('source_vertex_id'), self.hobby_vertex.get('id'))
        self.assertEqual(response.json().get('target_vertex_id'), self.person_vertex.get('id'))
        self.assertEqual(response.json().get('multi_edge'), True)

        person_vertex = self.client.get(
            f"/api/v1/projects/{self.project.get('id')}/vertices/{self.person_vertex.get('id')}")
        self.assertEqual(person_vertex.json().get('out_edges')[0].get('id'), self.performs_edge.get('id'))
        self.assertEqual(person_vertex.json().get('in_edges')[0].get('id'), response.json().get('id'))

        hobby_vertex = self.client.get(
            f"/api/v1/projects/{self.project.get('id')}/vertices/{self.hobby_vertex.get('id')}")
        self.assertEqual(hobby_vertex.json().get('out_edges')[0].get('id'), response.json().get('id'))
        self.assertEqual(hobby_vertex.json().get('in_edges')[0].get('id'), self.performs_edge.get('id'))

    def test_with_source_vertex_property_conflict(self):
        # Act
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/edges", json={
            'name': 'creates',
            'properties': [],
            'multi_edge': False,
            'source_vertex_id': self.person_vertex.get('id'),
            'target_vertex_id': self.hobby_vertex.get('id')
        })

        # Assume
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json().get('detail')[0].get('msg'),
                         "Edge name has conflict with property 'createsOut' of Source-Vertex")

    def test_with_target_vertex_property_conflict(self):
        # Act
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/edges", json={
            'name': 'checks',
            'properties': [],
            'multi_edge': True,
            'source_vertex_id': self.person_vertex.get('id'),
            'target_vertex_id': self.hobby_vertex.get('id')
        })

        # Assume
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json().get('detail')[0].get('msg'),
                         "Edge name has conflict with property 'checksIn' of Target-Vertex")
