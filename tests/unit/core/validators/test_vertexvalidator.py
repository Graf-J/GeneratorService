import unittest
import uuid

from app.core.entities import Vertex
from app.core.exceptions import DuplicateException
from app.core.validators import VertexValidator


class TestVertexValidator(unittest.TestCase):
    def setUp(self):
        uuid_1 = uuid.uuid4()
        uuid_2 = uuid.uuid4()

        self.vertex = Vertex(
            _id=str(uuid_1),
            name="Vertex",
            position_x=10,
            position_y=20,
            radius=5,
            properties=[]
        )

        self.other_vertex = Vertex(
            _id=str(2),
            name="OtherVertex",
            position_x=10,
            position_y=20,
            radius=5,
            properties=[]
        )

        self.duplicate_id_vertex = Vertex(
            _id=str(uuid_1),
            name="OtherVertex",
            position_x=10,
            position_y=20,
            radius=5,
            properties=[]
        )

        self.duplicate_name_vertex = Vertex(
            _id=str(uuid_2),
            name="Vertex",
            position_x=10,
            position_y=20,
            radius=5,
            properties=[]
        )

    def test_new_vertex_valid(self):
        # Arrange
        vertices = [self.vertex]
        new_vertex = self.other_vertex

        try:
            # Act
            VertexValidator.validate_new_vertex(vertices, new_vertex)
        except DuplicateException:
            # Assert
            self.fail('DuplicateException got raised despite no duplicates')

    def test_new_vertex_duplicate_id(self):
        # Arrange
        vertices = [self.vertex, self.other_vertex]
        new_vertex = self.duplicate_id_vertex

        # Act
        with self.assertRaises(DuplicateException) as context:
            VertexValidator.validate_new_vertex(vertices, new_vertex)

        # Assert
        self.assertEqual(context.exception.message, 'Vertex with Id already exists')

    def test_new_vertex_duplicate_name(self):
        # Arrange
        vertices = [self.vertex, self.other_vertex]
        new_vertex = self.duplicate_name_vertex

        # Act
        with self.assertRaises(DuplicateException) as context:
            VertexValidator.validate_new_vertex(vertices, new_vertex)

        # Assert
        self.assertEqual(context.exception.message, 'Vertex with Name already exists')
