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
            'source_vertex_id': self.person_vertex.get('id'),
            'target_vertex_id': self.hobby_vertex.get('id')
        })
        self.performs_edge = response.json()
        response = self.client.post(f"/api/v1/projects/{self.project.get('id')}/edges", json={
            'name': 'likes',
            'properties': [],
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
        response = self.client.put(f"/api/v1/projects/invalid-id/edges/{self.performs_edge.get('id')}", json={
            'name': 'new',
            'properties': [],
            'source_vertex_id': self.person_vertex.get('id'),
            'target_vertex_id': self.person_vertex.get('id')
        })

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'Project not found')

    def test_with_wrong_edge_id(self):
        # Act
        response = self.client.put(f"/api/v1/projects/{self.project.get('id')}/edges/invalid-id", json={
            'name': 'new',
            'properties': [],
            'source_vertex_id': self.person_vertex.get('id'),
            'target_vertex_id': self.person_vertex.get('id')
        })

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json().get('detail')[0].get('msg'), "Edge with Id 'invalid-id' not found")

    def test_with_wrong_target_vertex_id(self):
        # Arrange
        wrong_id = str(uuid.uuid4())

        # Act
        response = self.client.put(
            f"/api/v1/projects/{self.project.get('id')}/edges/{self.performs_edge.get('id')}",
            json={
                'name': 'new',
                'properties': [],
                'source_vertex_id': self.person_vertex.get('id'),
                'target_vertex_id': wrong_id
            })

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json().get('detail')[0].get('msg'), f"Vertex with Id '{wrong_id}' not found")

    def test_with_missing_name(self):
        # Act
        response = self.client.put(
            f"/api/v1/projects/{self.project.get('id')}/edges/{self.performs_edge.get('id')}",
            json={
                'properties': [],
                'source_vertex_id': self.person_vertex.get('id'),
                'target_vertex_id': self.person_vertex.get('id')
            })

        # Assert
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'Field required')

    def test_with_empty_name(self):
        # Act
        response = self.client.put(
            f"/api/v1/projects/{self.project.get('id')}/edges/{self.performs_edge.get('id')}",
            json={
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
        response = self.client.put(
            f"/api/v1/projects/{self.project.get('id')}/edges/{self.performs_edge.get('id')}",
            json={
                'name': '1new',
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
        response = self.client.put(
            f"/api/v1/projects/{self.project.get('id')}/edges/{self.performs_edge.get('id')}",
            json={
                'name': 'new-name',
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
        response = self.client.put(
            f"/api/v1/projects/{self.project.get('id')}/edges/{self.performs_edge.get('id')}",
            json={
                'name': 'new',
                'source_vertex_id': self.person_vertex.get('id'),
                'target_vertex_id': self.person_vertex.get('id')
            })

        # Assert
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'Field required')

    def test_with_minus_in_property_name(self):
        # Act
        response = self.client.put(
            f"/api/v1/projects/{self.project.get('id')}/edges/{self.performs_edge.get('id')}",
            json={
                'name': 'new',
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

    def test_with_missing_source_vertex_id(self):
        # Act
        response = self.client.put(
            f"/api/v1/projects/{self.project.get('id')}/edges/{self.performs_edge.get('id')}",
            json={
                'name': 'new',
                'properties': [],
                'target_vertex_id': self.person_vertex.get('id')
            })

        # Assert
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'Field required')

    def test_with_missing_target_vertex_id(self):
        # Act
        response = self.client.put(
            f"/api/v1/projects/{self.project.get('id')}/edges/{self.performs_edge.get('id')}",
            json={
                'name': 'new',
                'properties': [],
                'source_vertex_id': self.person_vertex.get('id')
            })

        # Assert
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json().get('detail')[0].get('msg'), 'Field required')

    def test_update_ordinary_edge_attributes(self):
        # Act
        response = self.client.put(
            f"/api/v1/projects/{self.project.get('id')}/edges/{self.performs_edge.get('id')}",
            json={
                'name': 'new_edge',
                'properties': [
                    {
                        'key': 'new_key',
                        'required': False,
                        'datatype': 'String'
                    }
                ],
                'source_vertex_id': self.person_vertex.get('id'),
                'target_vertex_id': self.hobby_vertex.get('id')
            })

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('id'), self.performs_edge.get('id'))
        self.assertEqual(response.json().get('name'), 'new_edge')
        self.assertEqual(len(response.json().get('properties')), 1)
        self.assertEqual(response.json().get('properties')[0].get('key'), 'new_key')
        self.assertEqual(response.json().get('properties')[0].get('required'), False)
        self.assertEqual(response.json().get('properties')[0].get('datatype'), 'String')

        person_vertex = self.client.get(
            f"api/v1/projects/{self.project.get('id')}/vertices/{self.person_vertex.get('id')}")
        self.assertEqual(person_vertex.json().get('out_edges')[1].get('id'), response.json().get('id'))
        self.assertEqual(person_vertex.json().get('out_edges')[1].get('name'), 'new_edge')

        hobby_vertex = self.client.get(
            f"api/v1/projects/{self.project.get('id')}/vertices/{self.hobby_vertex.get('id')}")
        self.assertEqual(hobby_vertex.json().get('in_edges')[0].get('id'), response.json().get('id'))
        self.assertEqual(hobby_vertex.json().get('in_edges')[0].get('name'), 'new_edge')

    def test_update_recursive_edge_attributes(self):
        # Act
        response = self.client.put(
            f"/api/v1/projects/{self.project.get('id')}/edges/{self.likes_edge.get('id')}",
            json={
                'name': 'new_edge',
                'properties': [
                    {
                        'key': 'new_key',
                        'required': False,
                        'datatype': 'String'
                    }
                ],
                'source_vertex_id': self.person_vertex.get('id'),
                'target_vertex_id': self.person_vertex.get('id')
            })

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('id'), self.likes_edge.get('id'))
        self.assertEqual(response.json().get('name'), 'new_edge')
        self.assertEqual(len(response.json().get('properties')), 1)
        self.assertEqual(response.json().get('properties')[0].get('key'), 'new_key')
        self.assertEqual(response.json().get('properties')[0].get('required'), False)
        self.assertEqual(response.json().get('properties')[0].get('datatype'), 'String')

        person_vertex = self.client.get(
            f"api/v1/projects/{self.project.get('id')}/vertices/{self.person_vertex.get('id')}")
        self.assertEqual(person_vertex.json().get('out_edges')[1].get('id'), response.json().get('id'))
        self.assertEqual(person_vertex.json().get('out_edges')[1].get('name'), 'new_edge')
        self.assertEqual(person_vertex.json().get('in_edges')[0].get('id'), response.json().get('id'))
        self.assertEqual(person_vertex.json().get('in_edges')[0].get('name'), 'new_edge')

    def test_update_ordinary_edge_name_to_duplicate(self):
        # Act
        response = self.client.put(
            f"/api/v1/projects/{self.project.get('id')}/edges/{self.performs_edge.get('id')}",
            json={
                'name': 'likes',
                'properties': [],
                'source_vertex_id': self.person_vertex.get('id'),
                'target_vertex_id': self.hobby_vertex.get('id')
            })

        # Assert
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json().get('detail')[0].get('msg'),
                         "Source-Vertex already has an outgoing edge with name 'likes'")

    def test_update_recursive_edge_name_to_duplicate(self):
        # Act
        response = self.client.put(
            f"/api/v1/projects/{self.project.get('id')}/edges/{self.likes_edge.get('id')}",
            json={
                'name': 'performs',
                'properties': [],
                'source_vertex_id': self.person_vertex.get('id'),
                'target_vertex_id': self.hobby_vertex.get('id')
            })

        # Assert
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json().get('detail')[0].get('msg'),
                         "Source-Vertex already has an outgoing edge with name 'performs'")

    def test_redirect_ordinary_edge_to_recursive(self):
        # Act
        response = self.client.put(
            f"/api/v1/projects/{self.project.get('id')}/edges/{self.performs_edge.get('id')}",
            json={
                'name': 'performs',
                'properties': [],
                'source_vertex_id': self.person_vertex.get('id'),
                'target_vertex_id': self.person_vertex.get('id')
            })

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('id'), self.performs_edge.get('id'))
        self.assertEqual(response.json().get('name'), 'performs')
        self.assertEqual(len(response.json().get('properties')), 0)

        person_vertex = self.client.get(
            f"api/v1/projects/{self.project.get('id')}/vertices/{self.person_vertex.get('id')}")
        self.assertEqual(person_vertex.json().get('out_edges')[1].get('id'), response.json().get('id'))
        self.assertEqual(person_vertex.json().get('out_edges')[1].get('name'), 'performs')
        self.assertEqual(person_vertex.json().get('in_edges')[1].get('id'), response.json().get('id'))
        self.assertEqual(person_vertex.json().get('in_edges')[1].get('name'), 'performs')

    def test_redirect_recursive_edge_to_ordinary(self):
        # Act
        response = self.client.put(
            f"/api/v1/projects/{self.project.get('id')}/edges/{self.likes_edge.get('id')}",
            json={
                'name': 'likes',
                'properties': [],
                'source_vertex_id': self.person_vertex.get('id'),
                'target_vertex_id': self.hobby_vertex.get('id')
            })

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('id'), self.likes_edge.get('id'))
        self.assertEqual(response.json().get('name'), 'likes')
        self.assertEqual(len(response.json().get('properties')), 0)

        person_vertex = self.client.get(
            f"api/v1/projects/{self.project.get('id')}/vertices/{self.person_vertex.get('id')}")
        self.assertEqual(person_vertex.json().get('out_edges')[1].get('id'), response.json().get('id'))
        self.assertEqual(person_vertex.json().get('out_edges')[1].get('name'), 'likes')

        hobby_vertex = self.client.get(
            f"api/v1/projects/{self.project.get('id')}/vertices/{self.hobby_vertex.get('id')}")
        self.assertEqual(hobby_vertex.json().get('in_edges')[1].get('id'), response.json().get('id'))
        self.assertEqual(hobby_vertex.json().get('in_edges')[1].get('name'), 'likes')

    def test_turn_around_ordinary_edge(self):
        # Act
        response = self.client.put(
            f"/api/v1/projects/{self.project.get('id')}/edges/{self.performs_edge.get('id')}",
            json={
                'name': 'performs',
                'properties': [],
                'source_vertex_id': self.hobby_vertex.get('id'),
                'target_vertex_id': self.person_vertex.get('id')
            })

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('id'), self.performs_edge.get('id'))
        self.assertEqual(response.json().get('name'), 'performs')
        self.assertEqual(len(response.json().get('properties')), 0)

        person_vertex = self.client.get(
            f"api/v1/projects/{self.project.get('id')}/vertices/{self.person_vertex.get('id')}")
        self.assertEqual(person_vertex.json().get('in_edges')[1].get('id'), response.json().get('id'))
        self.assertEqual(person_vertex.json().get('in_edges')[1].get('name'), 'performs')

        hobby_vertex = self.client.get(
            f"api/v1/projects/{self.project.get('id')}/vertices/{self.hobby_vertex.get('id')}")
        self.assertEqual(hobby_vertex.json().get('out_edges')[0].get('id'), response.json().get('id'))
        self.assertEqual(hobby_vertex.json().get('out_edges')[0].get('name'), 'performs')
