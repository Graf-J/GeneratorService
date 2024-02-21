import unittest
import uuid

from app.core.entities import Graph, Vertex, Edge
from app.core.exceptions import EdgeNotFoundException, VertexNotFoundException, VertexException


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
        with self.assertRaises(VertexNotFoundException) as context:
            self.graph.find_vertex_by_id('invalid-id')

        # Assert
        self.assertEqual(context.exception.message, "Vertex with Id 'invalid-id' not found")


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
        with self.assertRaises(VertexException) as context:
            self.graph.add_vertex(new_vertex)

        # Assert
        self.assertEqual(context.exception.message, f"Vertex with Id '{self.vertex_id}' already exists")

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
        with self.assertRaises(VertexException) as context:
            self.graph.add_vertex(new_vertex)

        # Assert
        self.assertEqual(context.exception.message, "Vertex with Name 'Test-Vertex' already exists")


class TestGraphFindEdgeById(unittest.TestCase):
    def setUp(self):
        self.vertex_id = str(uuid.uuid4())
        vertex = Vertex(
            _id=self.vertex_id,
            name='Test-Vertex',
            position_x=0,
            position_y=0,
            radius=20,
            properties=[],
        )

        self.edge_id = str(uuid.uuid4())
        self.edge = Edge(
            _id=self.edge_id,
            name='Edge-1',
            properties=[]
        )

        self.graph = Graph()
        self.graph.add_vertex(vertex)
        self.graph.add_edge(self.edge, self.vertex_id, self.vertex_id)

    def test_with_valid_id(self):
        # Act
        edge = self.graph.find_edge_by_id(self.edge_id)

        # Assert
        self.assertIsInstance(edge, Edge)
        self.assertEqual(edge.id, self.edge_id)

    def test_with_invalid_id(self):
        # Act
        with self.assertRaises(EdgeNotFoundException) as context:
            self.graph.find_edge_by_id('invalid-id')

        # Assert
        self.assertEqual(context.exception.message, "Edge with Id 'invalid-id' not found")


class TestGraphAddEdge(unittest.TestCase):
    def setUp(self):
        self.person_vertex_id = str(uuid.uuid4())
        self.person_vertex = Vertex(
            _id=self.person_vertex_id,
            name='Person',
            position_x=0,
            position_y=0,
            radius=20,
            properties=[],
        )
        self.hobby_vertex_id = str(uuid.uuid4())
        self.hobby_vertex = Vertex(
            _id=self.hobby_vertex_id,
            name='Hobby',
            position_x=0,
            position_y=0,
            radius=20,
            properties=[],
        )

        self.graph = Graph()
        self.graph.add_vertex(self.person_vertex)
        self.graph.add_vertex(self.hobby_vertex)

    def test_new_edge(self):
        # Arrange
        performs_edge_id = str(uuid.uuid4())
        performs_edge = Edge(
            _id=performs_edge_id,
            name='performs',
            properties=[]
        )

        # Act
        self.graph.add_edge(performs_edge, self.person_vertex_id, self.hobby_vertex_id)

        # Assert
        new_edge = self.graph.find_edge_by_id(performs_edge_id)
        self.assertEqual(id(new_edge), id(performs_edge))
        self.assertEqual(id(new_edge.source_vertex), id(self.person_vertex))
        self.assertEqual(id(new_edge.target_vertex), id(self.hobby_vertex))

    def test_new_edge_recursive(self):
        # Arrange
        likes_edge_id = str(uuid.uuid4())
        likes_edge = Edge(
            _id=likes_edge_id,
            name='likes',
            properties=[]
        )

        # Act
        self.graph.add_edge(likes_edge, self.person_vertex_id, self.person_vertex_id)

        new_edge = self.graph.find_edge_by_id(likes_edge_id)
        self.assertEqual(id(new_edge), id(likes_edge))
        self.assertEqual(id(new_edge.source_vertex), id(self.person_vertex))
        self.assertEqual(id(new_edge.target_vertex), id(self.person_vertex))
        self.assertEqual(id(new_edge.source_vertex), id(new_edge.target_vertex))
