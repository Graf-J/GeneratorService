import unittest
import uuid

from app.api.dto import VertexRequestDto, VertexResponseDto, EdgeResponseDto, PropertyDto
from app.core.entities import Graph, Vertex, Edge, Property
from app.mappers import VertexMapper


class TestVertexMapperToEntity(unittest.TestCase):
    def test_with_properties(self):
        # Arrange
        dto = VertexRequestDto(
            name="TestVertex",
            position_x=10,
            position_y=20,
            properties=[
                PropertyDto(key="name", required=False, datatype="String"),
                PropertyDto(key="age", required=True, datatype="Int"),
                PropertyDto(key="gpa", required=False, datatype="Float"),
                PropertyDto(key="married", required=False, datatype="Boolean")
            ]
        )

        # Act
        entity = VertexMapper.to_entity(dto)

        # Assert
        self.assertIsInstance(entity, Vertex)
        self.assertIsInstance(entity.id, str)
        self.assertEqual(entity.name, "TestVertex")
        self.assertEqual(entity.position_x, 10)
        self.assertEqual(entity.position_y, 20)
        self.assertEqual(len(entity.properties), 4)
        self.assertIsInstance(entity.properties[0], Property)
        self.assertIsInstance(entity.properties[1], Property)
        self.assertIsInstance(entity.properties[2], Property)
        self.assertIsInstance(entity.properties[3], Property)
        self.assertEqual(entity.properties[0].key, "name")
        self.assertEqual(entity.properties[0].required, False)
        self.assertEqual(entity.properties[0].datatype, "String")
        self.assertEqual(entity.properties[1].key, "age")
        self.assertEqual(entity.properties[1].required, True)
        self.assertEqual(entity.properties[1].datatype, "Int")
        self.assertEqual(entity.properties[2].key, "gpa")
        self.assertEqual(entity.properties[2].required, False)
        self.assertEqual(entity.properties[2].datatype, "Float")
        self.assertEqual(entity.properties[3].key, "married")
        self.assertEqual(entity.properties[3].required, False)
        self.assertEqual(entity.properties[3].datatype, "Boolean")

    def test_without_properties(self):
        # Arrange
        dto = VertexRequestDto(
            name="TestVertex",
            position_x=10,
            position_y=20,
            properties=[]
        )

        # Act
        entity = VertexMapper.to_entity(dto)

        # Assert
        self.assertIsInstance(entity, Vertex)
        self.assertIsInstance(entity.id, str)
        self.assertEqual(entity.name, "TestVertex")
        self.assertEqual(entity.position_x, 10)
        self.assertEqual(entity.position_y, 20)
        self.assertIsInstance(entity.properties, list)
        self.assertEqual(len(entity.properties), 0)


class TestVertexMapperToDto(unittest.TestCase):
    def test_with_properties(self):
        # Arrange
        vertex_id = uuid.uuid4()
        entity = Vertex(
            _id=str(vertex_id),
            name="TestVertex",
            position_x=10,
            position_y=20,
            properties=[
                Property(key="name", required=False, datatype="String"),
                Property(key="age", required=True, datatype="Int"),
                Property(key="gpa", required=False, datatype="Float"),
                Property(key="married", required=False, datatype="Boolean")
            ]
        )

        # Act
        dto = VertexMapper.to_dto(entity)

        # Assert
        self.assertIsInstance(dto, VertexResponseDto)
        self.assertEqual(dto.id, vertex_id)
        self.assertEqual(dto.name, "TestVertex")
        self.assertEqual(dto.position_x, 10)
        self.assertEqual(dto.position_y, 20)
        self.assertEqual(len(dto.properties), 4)
        self.assertIsInstance(dto.properties[0], PropertyDto)
        self.assertIsInstance(dto.properties[1], PropertyDto)
        self.assertIsInstance(dto.properties[2], PropertyDto)
        self.assertIsInstance(dto.properties[3], PropertyDto)
        self.assertEqual(dto.properties[0].key, "name")
        self.assertEqual(dto.properties[0].required, False)
        self.assertEqual(dto.properties[0].datatype, "String")
        self.assertEqual(dto.properties[1].key, "age")
        self.assertEqual(dto.properties[1].required, True)
        self.assertEqual(dto.properties[1].datatype, "Int")
        self.assertEqual(dto.properties[2].key, "gpa")
        self.assertEqual(dto.properties[2].required, False)
        self.assertEqual(dto.properties[2].datatype, "Float")
        self.assertEqual(dto.properties[3].key, "married")
        self.assertEqual(dto.properties[3].required, False)
        self.assertEqual(dto.properties[3].datatype, "Boolean")
        self.assertIsInstance(dto.out_edges, list)
        self.assertEqual(len(dto.out_edges), 0)
        self.assertIsInstance(dto.in_edges, list)
        self.assertEqual(len(dto.in_edges), 0)

    def test_without_properties(self):
        # Arrange
        vertex_id = uuid.uuid4()
        entity = Vertex(
            _id=str(vertex_id),
            name="TestVertex",
            position_x=10,
            position_y=20,
            properties=[]
        )

        # Act
        dto = VertexMapper.to_dto(entity)

        # Assert
        self.assertIsInstance(dto, VertexResponseDto)
        self.assertEqual(dto.id, vertex_id)
        self.assertEqual(dto.name, "TestVertex")
        self.assertEqual(dto.position_x, 10)
        self.assertEqual(dto.position_y, 20)
        self.assertEqual(len(dto.properties), 0)
        self.assertIsInstance(dto.properties, list)
        self.assertIsInstance(dto.out_edges, list)
        self.assertEqual(len(dto.out_edges), 0)
        self.assertIsInstance(dto.in_edges, list)
        self.assertEqual(len(dto.in_edges), 0)

    def test_with_edges(self):
        # Arrange
        vertex_id = uuid.uuid4()
        entity = Vertex(
            _id=str(vertex_id),
            name="TestVertex",
            position_x=10,
            position_y=20,
            properties=[]
        )
        edge_id = uuid.uuid4()
        edge = Edge(
            _id=str(edge_id),
            name="TestEdge",
            properties=[],
            multi_edge=True
        )
        graph = Graph()
        graph.add_vertex(entity)
        graph.add_edge(edge, str(vertex_id), str(vertex_id))

        # Act
        dto = VertexMapper.to_dto(entity)

        # Assert
        self.assertIsInstance(dto, VertexResponseDto)
        self.assertEqual(dto.id, vertex_id)
        self.assertEqual(dto.name, "TestVertex")
        self.assertEqual(dto.position_x, 10)
        self.assertEqual(dto.position_y, 20)
        self.assertIsInstance(dto.properties, list)
        self.assertEqual(len(dto.properties), 0)
        self.assertIsInstance(dto.out_edges, list)
        self.assertEqual(len(dto.out_edges), 1)
        self.assertIsInstance(dto.out_edges[0], EdgeResponseDto)
        self.assertEqual(dto.out_edges[0].id, edge_id)
        self.assertIsInstance(dto.in_edges, list)
        self.assertEqual(len(dto.in_edges), 1)
        self.assertEqual(dto.in_edges[0].id, edge_id)
