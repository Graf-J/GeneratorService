import unittest
import uuid

from app.api.dto import EdgeRequestDto, EdgeResponseDto, PropertyDto
from app.core.entities import Vertex, Edge, Property
from app.mappers import EdgeMapper


class TestEdgeMapperToEntity(unittest.TestCase):
    def test_with_properties(self):
        # Arrange
        dto = EdgeRequestDto(
            name='TestEdge',
            properties=[
                PropertyDto(key='TestProperty', required=True, datatype='String')
            ],
            source_vertex_id='ab02b44c-e95a-4645-80c9-2a5067dd671d',
            target_vertex_id='033633af-fed2-40a6-b7e3-138e3bfe421e'
        )

        # Act
        entity = EdgeMapper.to_entity(dto)

        # Assert
        self.assertIsInstance(entity, Edge)
        self.assertIsInstance(entity.id, str)
        self.assertEqual(entity.name, 'TestEdge')
        self.assertEqual(entity.source_vertex, None)
        self.assertEqual(entity.target_vertex, None)
        self.assertEqual(len(entity.properties), 1)
        self.assertEqual(entity.properties[0].key, 'TestProperty')
        self.assertEqual(entity.properties[0].required, True)
        self.assertEqual(entity.properties[0].datatype, 'String')

    def test_without_properties(self):
        # Arange
        dto = EdgeRequestDto(
            name='TestEdge',
            properties=[],
            source_vertex_id='ab02b44c-e95a-4645-80c9-2a5067dd671d',
            target_vertex_id='033633af-fed2-40a6-b7e3-138e3bfe421e'
        )

        # Act
        entity = EdgeMapper.to_entity(dto)

        # Assert
        self.assertIsInstance(entity, Edge)
        self.assertIsInstance(entity.id, str)
        self.assertEqual(entity.name, 'TestEdge')
        self.assertEqual(entity.source_vertex, None)
        self.assertEqual(entity.target_vertex, None)
        self.assertIsInstance(entity.properties, list)
        self.assertEqual(len(entity.properties), 0)


class TestEdgeMapperToDto(unittest.TestCase):
    def test_with_properties(self):
        # Arrange
        vertex_1_id = uuid.uuid4()
        vertex_1 = Vertex(
            _id=str(vertex_1_id),
            name="Vertex1",
            position_x=10,
            position_y=20,
            radius=5,
            properties=[]
        )
        vertex_2_id = uuid.uuid4()
        vertex_2 = Vertex(
            _id=str(vertex_2_id),
            name="Vertex1",
            position_x=10,
            position_y=20,
            radius=5,
            properties=[]
        )

        edge_id = uuid.uuid4()
        entity = Edge(
            _id=str(edge_id),
            name='TestEdge',
            properties=[
                Property(key='TestProperty', required=True, datatype='String')
            ],
        )
        entity.source_vertex = vertex_1
        entity.target_vertex = vertex_2

        # Act
        dto = EdgeMapper.to_dto(entity)

        # Assert
        self.assertIsInstance(dto, EdgeResponseDto)
        self.assertEqual(dto.id, edge_id)
        self.assertEqual(dto.name, 'TestEdge')
        self.assertEqual(dto.source_vertex_id, vertex_1_id)
        self.assertEqual(dto.target_vertex_id, vertex_2_id)
        self.assertEqual(len(dto.properties), 1)
        self.assertIsInstance(dto.properties[0], PropertyDto)
        self.assertEqual(dto.properties[0].key, 'TestProperty')
        self.assertEqual(dto.properties[0].required, True)
        self.assertEqual(dto.properties[0].datatype, 'String')

    def test_without_properties(self):
        # Arrange
        vertex_1_id = uuid.uuid4()
        vertex_1 = Vertex(
            _id=str(vertex_1_id),
            name="Vertex1",
            position_x=10,
            position_y=20,
            radius=5,
            properties=[]
        )
        vertex_2_id = uuid.uuid4()
        vertex_2 = Vertex(
            _id=str(vertex_2_id),
            name="Vertex1",
            position_x=10,
            position_y=20,
            radius=5,
            properties=[]
        )

        edge_id = uuid.uuid4()
        entity = Edge(
            _id=str(edge_id),
            name='TestEdge',
            properties=[],
        )
        entity.source_vertex = vertex_1
        entity.target_vertex = vertex_2

        # Act
        dto = EdgeMapper.to_dto(entity)

        # Assert
        self.assertIsInstance(dto, EdgeResponseDto)
        self.assertEqual(dto.id, edge_id)
        self.assertEqual(dto.name, 'TestEdge')
        self.assertEqual(dto.source_vertex_id, vertex_1_id)
        self.assertEqual(dto.target_vertex_id, vertex_2_id)
        self.assertIsInstance(dto.properties, list)
        self.assertEqual(len(dto.properties), 0)
