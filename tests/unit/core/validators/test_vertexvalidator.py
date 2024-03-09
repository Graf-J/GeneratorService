import unittest
import uuid

from app.core.entities import Vertex
from app.core.exceptions import VertexException
from app.core.validators import VertexValidator


class TestVertexValidator(unittest.TestCase):
    def setUp(self):
        self.first_vertex_id = str(uuid.uuid4())
        self.first_vertex = Vertex(
            _id=self.first_vertex_id,
            name="FirstVertex",
            position_x=10,
            position_y=20,
            properties=[]
        )
        self.second_vertex_id = str(uuid.uuid4())
        self.second_vertex = Vertex(
            _id=self.second_vertex_id,
            name="SecondVertex",
            position_x=10,
            position_y=20,
            properties=[]
        )

    def test_new_vertex_valid(self):
        # Arrange
        vertices = [self.first_vertex]

        try:
            # Act
            VertexValidator.validate_new_vertex(vertices, self.second_vertex)
        except VertexException:
            # Assert
            self.fail('Operation should not raise an Exception')

    def test_new_vertex_with_duplicate_id(self):
        # Arrange
        duplicate_id_vertex = Vertex(
            _id=self.second_vertex_id,
            name="NewVertex",
            position_x=20,
            position_y=43,
            properties=[]
        )
        vertices = [self.first_vertex, self.second_vertex]

        # Act
        with self.assertRaises(VertexException) as context:
            VertexValidator.validate_new_vertex(vertices, duplicate_id_vertex)

        # Assert
        self.assertEqual(context.exception.message, f"Vertex with Id '{self.second_vertex_id}' already exists")

    def test_new_vertex_with_duplicate_name(self):
        # Arrange
        duplicate_name_vertex = Vertex(
            _id=str(uuid.uuid4()),
            name=self.second_vertex.name,
            position_x=20,
            position_y=43,
            properties=[]
        )
        vertices = [self.first_vertex, self.second_vertex]

        # Act
        with self.assertRaises(VertexException) as context:
            VertexValidator.validate_new_vertex(vertices, duplicate_name_vertex)

        # Assert
        self.assertEqual(context.exception.message, f"Vertex with Name '{self.second_vertex.name}' already exists")
