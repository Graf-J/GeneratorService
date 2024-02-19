import unittest
import uuid

from app.core.entities import Graph, Vertex
from app.core.exceptions import NotFoundException, DuplicateException


class TestGraphFindVertexById(unittest.TestCase):
    def setUp(self):
        self.id_1 = str(uuid.uuid4())
        self.vertex_1 = Vertex(
            _id=self.id_1,
            name='Vertex-1',
            position_x=0,
            position_y=0,
            radius=20,
            properties=[],
        )

        self.id_2 = str(uuid.uuid4())
        self.vertex_2 = Vertex(
            _id=self.id_2,
            name='Vertex-2',
            position_x=30,
            position_y=30,
            radius=15,
            properties=[],
        )

        self.graph = Graph()
        self.graph.add_vertex(self.vertex_1)
        self.graph.add_vertex(self.vertex_2)

    def test_with_valid_id(self):
        # Act
        vertex = self.graph.find_vertex_by_id(self.id_2)

        # Assert
        self.assertIsInstance(vertex, Vertex)
        self.assertEqual(vertex.id, self.id_2)

    def test_with_invalid_id(self):
        # Act
        with self.assertRaises(NotFoundException) as context:
            self.graph.find_vertex_by_id('invalid-id')

        # Assert
        self.assertEqual(context.exception.message, 'Vertex with Id not found')


class TestGraphAddVertex(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        self.vertex_id = str(uuid.uuid4())
        vertex = Vertex(
            _id=self.vertex_id,
            name='Test-Vertex',
            position_x=0,
            position_y=0,
            radius=20,
            properties=[],
        )
        self.graph.add_vertex(vertex)

    def test_valid_vertex(self):
        # Arrange
        new_vertex = Vertex(
            _id=str(uuid.uuid4()),
            name='New-Vertex',
            position_x=0,
            position_y=0,
            radius=20,
            properties=[],
        )

        # Act
        self.graph.add_vertex(new_vertex)

        # Assume
        self.assertEqual(len(self.graph.vertices), 2)

    def test_duplicate_id_vertex(self):
        # Arrange
        new_vertex = Vertex(
            _id=self.vertex_id,
            name='New-Vertex',
            position_x=0,
            position_y=0,
            radius=20,
            properties=[],
        )

        # Act
        with self.assertRaises(DuplicateException) as context:
            self.graph.add_vertex(new_vertex)

        # Assert
        self.assertEqual(context.exception.message, 'Vertex with Id already exists')

    def test_duplicate_name_vertex(self):
        # Arrange
        new_vertex = Vertex(
            _id=str(uuid.uuid4()),
            name='Test-Vertex',
            position_x=0,
            position_y=0,
            radius=20,
            properties=[],
        )

        # Act
        with self.assertRaises(DuplicateException) as context:
            self.graph.add_vertex(new_vertex)

        # Assert
        self.assertEqual(context.exception.message, 'Vertex with Name already exists')
