import unittest
import uuid

from app.core.entities import Graph, Vertex, Edge, Property
from app.core.entities.property import Datatype
from app.core.exceptions import EdgeException
from app.core.validators import EdgeValidator


class TestEdgeValidatorValidateNewEdgeWithExistingOutEdgeAndNewVertex(unittest.TestCase):
    def setUp(self):
        # Vertices
        self.person_vertex = Vertex(
            _id=str(uuid.uuid4()),
            name='Person',
            position_x=0,
            position_y=0,
            radius=20,
            properties=[],
        )
        self.hobby_vertex = Vertex(
            _id=str(uuid.uuid4()),
            name='Hobby',
            position_x=0,
            position_y=0,
            radius=20,
            properties=[],
        )
        self.new_vertex = Vertex(
            _id=str(uuid.uuid4()),
            name='New-Vertex',
            position_x=0,
            position_y=0,
            radius=20,
            properties=[],
        )
        # Edges
        self.performs_edge = Edge(
            _id=str(uuid.uuid4()),
            name='performs',
            properties=[]
        )
        self.new_performs_edge = Edge(
            _id=str(uuid.uuid4()),
            name='performs',
            properties=[]
        )
        self.new_likes_edge = Edge(
            _id=str(uuid.uuid4()),
            name='likes',
            properties=[]
        )
        # Build Graph
        self.graph = Graph()
        self.graph.add_vertex(self.person_vertex)
        self.graph.add_vertex(self.hobby_vertex)
        self.graph.add_vertex(self.new_vertex)
        self.graph.add_edge(self.performs_edge, self.person_vertex.id, self.hobby_vertex.id)

    def test_out_edge_with_same_name(self):
        # Act
        with self.assertRaises(EdgeException) as context:
            EdgeValidator.validate_new_edge_name(self.new_performs_edge.name, self.person_vertex.out_edges,
                                                 self.new_vertex.in_edges)

        # Assert
        self.assertEqual(context.exception.message,
                         "Vertex already has an outgoing edge with name 'performs'")

    def test_out_edge_with_different_name(self):
        try:
            # Act
            EdgeValidator.validate_new_edge_name(self.new_likes_edge.name, self.person_vertex.out_edges,
                                                 self.new_vertex.in_edges)
        except EdgeException:
            # Assume
            self.fail('Operation should now throw an exception')

    def test_in_edge_with_same_name(self):
        try:
            # Act
            EdgeValidator.validate_new_edge_name(self.new_performs_edge.name, self.new_vertex.out_edges,
                                                 self.person_vertex.in_edges)
        except EdgeException:
            # Assume
            self.fail('Operation should now throw an exception')

    def test_in_edge_with_different_name(self):
        try:
            # Act
            EdgeValidator.validate_new_edge_name(self.new_likes_edge.name, self.new_vertex.out_edges,
                                                 self.person_vertex.in_edges)
        except EdgeException:
            # Assume
            self.fail('Operation should now throw an exception')


class TestEdgeValidatorValidateNewEdgeWithExistingInEdgeAndNewVertex(unittest.TestCase):
    def setUp(self):
        # Vertices
        self.person_vertex = Vertex(
            _id=str(uuid.uuid4()),
            name='Person',
            position_x=0,
            position_y=0,
            radius=20,
            properties=[],
        )
        self.hobby_vertex = Vertex(
            _id=str(uuid.uuid4()),
            name='Hobby',
            position_x=0,
            position_y=0,
            radius=20,
            properties=[],
        )
        self.new_vertex = Vertex(
            _id=str(uuid.uuid4()),
            name='New-Vertex',
            position_x=0,
            position_y=0,
            radius=20,
            properties=[],
        )
        # Edges
        self.performs_edge = Edge(
            _id=str(uuid.uuid4()),
            name='performs',
            properties=[]
        )
        self.new_performs_edge = Edge(
            _id=str(uuid.uuid4()),
            name='performs',
            properties=[]
        )
        self.new_likes_edge = Edge(
            _id=str(uuid.uuid4()),
            name='likes',
            properties=[]
        )
        # Build Graph
        self.graph = Graph()
        self.graph.add_vertex(self.person_vertex)
        self.graph.add_vertex(self.hobby_vertex)
        self.graph.add_vertex(self.new_vertex)
        self.graph.add_edge(self.performs_edge, self.person_vertex.id, self.hobby_vertex.id)

    def test_out_edge_with_same_name(self):
        try:
            # Act
            EdgeValidator.validate_new_edge_name(self.new_performs_edge.name, self.hobby_vertex.out_edges,
                                                 self.new_vertex.in_edges)
        except EdgeException:
            # Assume
            self.fail('Operation should now throw an exception')

    def test_out_edge_with_different_name(self):
        try:
            # Act
            EdgeValidator.validate_new_edge_name(self.new_likes_edge.name, self.hobby_vertex.out_edges,
                                                 self.new_vertex.in_edges)
        except EdgeException:
            # Assume
            self.fail('Operation should now throw an exception')

    def test_in_edge_with_same_name(self):
        # Act
        with self.assertRaises(EdgeException) as context:
            EdgeValidator.validate_new_edge_name(self.new_performs_edge.name, self.new_vertex.out_edges,
                                                 self.hobby_vertex.in_edges)

        # Assert
        self.assertEqual(context.exception.message,
                         "Vertex already has an incoming edge with name 'performs'")

    def test_in_edge_with_different_name(self):
        try:
            # Act
            EdgeValidator.validate_new_edge_name(self.new_likes_edge.name, self.new_vertex.out_edges,
                                                 self.hobby_vertex.in_edges)
        except EdgeException:
            # Assume
            self.fail('Operation should now throw an exception')


class TestEdgeValidatorValidateNewEdgeWithExistingOutEdgeAndSameVertex(unittest.TestCase):
    def setUp(self):
        # Vertices
        self.person_vertex = Vertex(
            _id=str(uuid.uuid4()),
            name='Person',
            position_x=0,
            position_y=0,
            radius=20,
            properties=[],
        )
        self.hobby_vertex = Vertex(
            _id=str(uuid.uuid4()),
            name='Hobby',
            position_x=0,
            position_y=0,
            radius=20,
            properties=[],
        )
        # Edges
        self.performs_edge = Edge(
            _id=str(uuid.uuid4()),
            name='performs',
            properties=[]
        )
        self.new_performs_edge = Edge(
            _id=str(uuid.uuid4()),
            name='performs',
            properties=[]
        )
        self.new_likes_edge = Edge(
            _id=str(uuid.uuid4()),
            name='likes',
            properties=[]
        )
        # Build Graph
        self.graph = Graph()
        self.graph.add_vertex(self.person_vertex)
        self.graph.add_vertex(self.hobby_vertex)
        self.graph.add_edge(self.performs_edge, self.person_vertex.id, self.hobby_vertex.id)

    def test_out_edge_with_same_name(self):
        # Act
        with self.assertRaises(EdgeException) as context:
            EdgeValidator.validate_new_edge_name(self.new_performs_edge.name, self.person_vertex.out_edges,
                                                 self.hobby_vertex.in_edges)

        # Assert
        self.assertEqual(context.exception.message,
                         "Vertex already has an outgoing edge with name 'performs'")

    def test_out_edge_with_different_name(self):
        try:
            # Act
            EdgeValidator.validate_new_edge_name(self.new_likes_edge.name, self.person_vertex.out_edges,
                                                 self.hobby_vertex.in_edges)
        except EdgeException:
            # Assume
            self.fail('Operation should now throw an exception')

    def test_in_edge_with_same_name(self):
        try:
            # Act
            EdgeValidator.validate_new_edge_name(self.new_performs_edge.name, self.hobby_vertex.out_edges,
                                                 self.person_vertex.in_edges)
        except EdgeException:
            # Assume
            self.fail('Operation should now throw an exception')

    def test_in_edge_with_different_name(self):
        try:
            # Act
            EdgeValidator.validate_new_edge_name(self.new_likes_edge.name, self.hobby_vertex.out_edges,
                                                 self.person_vertex.in_edges)
        except EdgeException:
            # Assume
            self.fail('Operation should now throw an exception')


class TestEdgeValidatorValidateNewEdgeWithExistingInEdgeAndSameVertex(unittest.TestCase):
    def setUp(self):
        # Vertices
        self.person_vertex = Vertex(
            _id=str(uuid.uuid4()),
            name='Person',
            position_x=0,
            position_y=0,
            radius=20,
            properties=[],
        )
        self.hobby_vertex = Vertex(
            _id=str(uuid.uuid4()),
            name='Hobby',
            position_x=0,
            position_y=0,
            radius=20,
            properties=[],
        )
        # Edges
        self.performs_edge = Edge(
            _id=str(uuid.uuid4()),
            name='performs',
            properties=[]
        )
        self.new_performs_edge = Edge(
            _id=str(uuid.uuid4()),
            name='performs',
            properties=[]
        )
        self.new_likes_edge = Edge(
            _id=str(uuid.uuid4()),
            name='likes',
            properties=[]
        )
        # Build Graph
        self.graph = Graph()
        self.graph.add_vertex(self.person_vertex)
        self.graph.add_vertex(self.hobby_vertex)
        self.graph.add_edge(self.performs_edge, self.person_vertex.id, self.hobby_vertex.id)

    def test_out_edge_with_same_name(self):
        try:
            # Act
            EdgeValidator.validate_new_edge_name(self.new_performs_edge.name, self.hobby_vertex.out_edges,
                                                 self.person_vertex.in_edges)
        except EdgeException:
            # Assume
            self.fail('Operation should now throw an exception')

    def test_out_edge_with_different_name(self):
        try:
            # Act
            EdgeValidator.validate_new_edge_name(self.new_likes_edge.name, self.hobby_vertex.out_edges,
                                                 self.person_vertex.in_edges)
        except EdgeException:
            # Assume
            self.fail('Operation should now throw an exception')

    def test_in_edge_with_same_name(self):
        # Act
        with self.assertRaises(EdgeException) as context:
            EdgeValidator.validate_new_edge_name(self.new_performs_edge.name, self.person_vertex.out_edges,
                                                 self.hobby_vertex.in_edges)

        # Assert
        self.assertEqual(context.exception.message,
                         "Vertex already has an outgoing edge with name 'performs'")

    def test_in_edge_with_different_name(self):
        try:
            # Act
            EdgeValidator.validate_new_edge_name(self.new_likes_edge.name, self.person_vertex.out_edges,
                                                 self.hobby_vertex.in_edges)
        except EdgeException:
            # Assume
            self.fail('Operation should now throw an exception')


class TestEdgeValidatorValidateNewEdgeWithRecursion(unittest.TestCase):
    def setUp(self):
        # Vertices
        self.person_vertex = Vertex(
            _id=str(uuid.uuid4()),
            name='Person',
            position_x=0,
            position_y=0,
            radius=20,
            properties=[],
        )
        self.hobby_vertex = Vertex(
            _id=str(uuid.uuid4()),
            name='Hobby',
            position_x=0,
            position_y=0,
            radius=20,
            properties=[],
        )
        # Edges
        self.likes_edge = Edge(
            _id=str(uuid.uuid4()),
            name='likes',
            properties=[]
        )
        self.new_likes_edge = Edge(
            _id=str(uuid.uuid4()),
            name='likes',
            properties=[]
        )
        self.new_performs_edge = Edge(
            _id=str(uuid.uuid4()),
            name='performs',
            properties=[]
        )
        # Build Graph
        self.graph = Graph()
        self.graph.add_vertex(self.person_vertex)
        self.graph.add_vertex(self.hobby_vertex)

    def test_one_recursive_edge(self):
        try:
            # Act
            EdgeValidator.validate_new_edge_name(self.likes_edge.name, self.person_vertex.out_edges,
                                                 self.person_vertex.in_edges)
        except EdgeException:
            # Assert
            self.fail('Operation should now throw an exception')

    def test_two_recursive_edges_with_same_name(self):
        # Arrange
        self.graph.add_edge(self.likes_edge, self.person_vertex.id, self.person_vertex.id)

        # Act
        with self.assertRaises(EdgeException) as context:
            EdgeValidator.validate_new_edge_name(self.new_likes_edge.name, self.person_vertex.out_edges,
                                                 self.person_vertex.in_edges)

        # Assume
        self.assertEqual(context.exception.message, "Vertex already has an outgoing edge with name 'likes'")

    def test_two_recursive_edges_with_different_name(self):
        # Arrange
        self.graph.add_edge(self.likes_edge, self.person_vertex.id, self.person_vertex.id)

        try:
            # Act
            EdgeValidator.validate_new_edge_name(self.new_performs_edge.name, self.person_vertex.out_edges,
                                                 self.person_vertex.in_edges)
        except EdgeException:
            # Assert
            self.fail('Operation should now throw an exception')

    def test_one_recursive_edge_plus_edge_with_same_name_to_other_vertex(self):
        # Arrange
        self.graph.add_edge(self.likes_edge, self.person_vertex.id, self.person_vertex.id)

        # Act
        with self.assertRaises(EdgeException) as context:
            EdgeValidator.validate_new_edge_name(self.new_likes_edge.name, self.person_vertex.out_edges,
                                                 self.hobby_vertex.in_edges)

        # Assume
        self.assertEqual(context.exception.message, "Vertex already has an outgoing edge with name 'likes'")

    def test_one_recursive_edge_plus_edge_with_other_name_to_other_vertex(self):
        # Arrange
        self.graph.add_edge(self.likes_edge, self.person_vertex.id, self.person_vertex.id)

        try:
            # Act
            EdgeValidator.validate_new_edge_name(self.new_performs_edge.name, self.person_vertex.out_edges,
                                                 self.hobby_vertex.in_edges)
        except EdgeException:
            # Assert
            self.fail('Operation should now throw an exception')

    def test_one_recursive_edge_plus_edge_with_same_name_from_other_vertex(self):
        # Arrange
        self.graph.add_edge(self.likes_edge, self.person_vertex.id, self.person_vertex.id)

        # Act
        with self.assertRaises(EdgeException) as context:
            EdgeValidator.validate_new_edge_name(self.new_likes_edge.name, self.hobby_vertex.out_edges,
                                                 self.person_vertex.in_edges)

        # Assume
        self.assertEqual(context.exception.message, "Vertex already has an incoming edge with name 'likes'")

    def test_one_recursive_edge_plus_edge_with_other_name_from_other_vertex(self):
        # Arrange
        self.graph.add_edge(self.likes_edge, self.person_vertex.id, self.person_vertex.id)

        try:
            # Act
            EdgeValidator.validate_new_edge_name(self.new_performs_edge.name, self.hobby_vertex.out_edges,
                                                 self.person_vertex.in_edges)
        except EdgeException:
            # Assert
            self.fail('Operation should now throw an exception')


class TestValidateConnectVerticesProperties(unittest.TestCase):
    def test_with_conflicting_source_vertex_property(self):
        # Arrange
        source_vertex_properties = [
            Property(key='nameOut', required=True, datatype=Datatype.STRING),
            Property(key='age', required=False, datatype=Datatype.INT)
        ]
        target_vertex_properties = [
            Property(key='key', required=True, datatype=Datatype.FLOAT)
        ]

        # Act
        with self.assertRaises(EdgeException) as context:
            EdgeValidator.validate_connected_vertices_properties(
                'name',
                source_vertex_properties,
                target_vertex_properties
            )

        # Assert
        self.assertEqual(context.exception.message, "Edge name has conflict with property 'nameOut' of source vertex")

    def test_with_conflicting_target_vertex_property(self):
        # Arrange
        source_vertex_properties = [
            Property(key='name', required=True, datatype=Datatype.STRING),
            Property(key='age', required=False, datatype=Datatype.INT)
        ]
        target_vertex_properties = [
            Property(key='keyIn', required=True, datatype=Datatype.FLOAT)
        ]

        # Act
        with self.assertRaises(EdgeException) as context:
            EdgeValidator.validate_connected_vertices_properties(
                'key',
                source_vertex_properties,
                target_vertex_properties
            )

        # Assert
        self.assertEqual(context.exception.message, "Edge name has conflict with property 'keyIn' of target vertex")

    def test_with_valid_properties(self):
        # Arrange
        source_vertex_properties = [
            Property(key='name', required=True, datatype=Datatype.STRING),
            Property(key='age', required=False, datatype=Datatype.INT)
        ]
        target_vertex_properties = [
            Property(key='key', required=True, datatype=Datatype.FLOAT)
        ]

        # Act
        EdgeValidator.validate_connected_vertices_properties(
            'name',
            source_vertex_properties,
            target_vertex_properties
        )
