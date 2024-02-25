import unittest

from app.core.entities import Vertex, Property
from app.core.entities.property import Datatype


class TestVertexToDict(unittest.TestCase):
    def test(self):
        # Arrange
        vertex = Vertex(
            _id='1',
            name='MyVertex',
            position_x=10,
            position_y=20,
            radius=30,
            properties=[
                Property(key='name', required=True, datatype=Datatype.STRING),
                Property(key='age', required=False, datatype=Datatype.INT)
            ]
        )

        # Act
        vertex_dict = vertex.to_dict()

        # Assert
        expected = {
            'id': '1',
            'label': 'MyVertex',
            'single_field_name': 'myVertex',
            'multiple_field_name': 'myVertexList',
            'properties': [
                {'field_name': 'name'},
                {'field_name': 'age'}
            ]
        }
        self.assertEqual(vertex_dict, expected)
