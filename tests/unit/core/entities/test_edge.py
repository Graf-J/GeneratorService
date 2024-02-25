import unittest

from app.core.entities import Vertex, Edge, Property
from app.core.entities.property import Datatype


class TestEdgeToDict(unittest.TestCase):
    def test(self):
        # Arrange
        vertex = Vertex(
            _id='1',
            name='MyVertex',
            position_x=10,
            position_y=20,
            radius=30,
            properties=[]
        )
        edge = Edge(
            _id='2',
            name='MyEdge',
            properties=[
                Property(key='strength', required=True, datatype=Datatype.FLOAT),
                Property(key='isMarried', required=False, datatype=Datatype.BOOLEAN)
            ],
            multi_edge=True
        )
        edge.source_vertex = vertex
        edge.target_vertex = vertex

        # Act
        edge_dict = edge.to_dict()

        # Assert
        expected = {
            'label': 'MyEdge',
            'out_field_name': 'myEdgeOut',
            'in_field_name': 'myEdgeIn',
            'source_vertex_id': '1',
            'target_vertex_id': '1',
            'multi_edge': True,
            'properties': [
                {'field_name': 'strength'},
                {'field_name': 'isMarried'}
            ]
        }
        self.assertEqual(edge_dict, expected)
