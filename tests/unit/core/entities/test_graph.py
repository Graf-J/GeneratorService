import unittest
import uuid

from app.core.entities import Graph, Vertex, Edge, Property
from app.core.entities.property import Datatype
from app.core.exceptions import EdgeNotFoundException, VertexNotFoundException, VertexException, EdgeException


class TestGraphFindVertexById(unittest.TestCase):
    def setUp(self):
        self.id_1 = str(uuid.uuid4())
        self.vertex_1 = Vertex(
            _id=self.id_1,
            name='Vertex1',
            position_x=0,
            position_y=0,
            radius=20,
            properties=[],
        )

        self.id_2 = str(uuid.uuid4())
        self.vertex_2 = Vertex(
            _id=self.id_2,
            name='Vertex2',
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
            name='TestVertex',
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
            name='NewVertex',
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
            name='NewVertex',
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
            name='TestVertex',
            position_x=0,
            position_y=0,
            radius=20,
            properties=[],
        )

        # Act
        with self.assertRaises(VertexException) as context:
            self.graph.add_vertex(new_vertex)

        # Assert
        self.assertEqual(context.exception.message, "Vertex with Name 'TestVertex' already exists")


class TestGraphUpdateVertex(unittest.TestCase):
    def setUp(self):
        # Vertices
        self.person_vertex_id = str(uuid.uuid4())
        self.person_vertex = Vertex(
            _id=self.person_vertex_id,
            name='Person',
            position_x=0,
            position_y=0,
            radius=20,
            properties=[Property(key='name', required=True, datatype=Datatype.STRING)]
        )
        self.hobby_vertex_id = str(uuid.uuid4())
        self.hobby_vertex = Vertex(
            _id=self.hobby_vertex_id,
            name='Hobby',
            position_x=0,
            position_y=0,
            radius=20,
            properties=[]
        )
        # Edge
        self.performs_edge_id = str(uuid.uuid4())
        self.performs_edge = Edge(
            _id=self.performs_edge_id,
            name='performs',
            properties=[],
            multi_edge=False
        )
        # Build Graph
        self.graph = Graph()
        self.graph.add_vertex(self.person_vertex)
        self.graph.add_vertex(self.hobby_vertex)
        self.graph.add_edge(self.performs_edge, self.person_vertex_id, self.hobby_vertex_id)

    def test_with_invalid_vertex_id(self):
        # Arrange
        new_vertex = Vertex(
            _id='',
            name='Surgery',
            position_x=10,
            position_y=10,
            radius=30,
            properties=[]
        )

        # Act
        with self.assertRaises(VertexNotFoundException) as context:
            self.graph.update_vertex('invalid-id', new_vertex)

        # Assert
        self.assertEqual(context.exception.message, "Vertex with Id 'invalid-id' not found")

    def test_with_duplicate_name(self):
        # Arrange
        new_vertex = Vertex(
            _id='',
            name='Person',
            position_x=10,
            position_y=10,
            radius=30,
            properties=[]
        )

        # Act
        with self.assertRaises(VertexException) as context:
            self.graph.update_vertex(self.hobby_vertex_id, new_vertex)

        # Assert
        self.assertEqual(context.exception.message, "Vertex with Name 'Person' already exists")
        self.assertEqual(self.graph.find_vertex_by_id(self.hobby_vertex_id).name, 'Hobby')

    def test_with_new_attributes(self):
        # Arrange
        new_vertex = Vertex(
            _id='',
            name='Surgery',
            position_x=10,
            position_y=10,
            radius=30,
            properties=[]
        )

        # Act
        self.graph.update_vertex(self.hobby_vertex_id, new_vertex)

        # Assert
        updated_vertex = self.graph.find_vertex_by_id(self.hobby_vertex_id)
        self.assertEqual(updated_vertex.id, self.hobby_vertex_id)
        self.assertEqual(updated_vertex.name, 'Surgery')
        self.assertEqual(updated_vertex.position_x, 10)
        self.assertEqual(updated_vertex.position_y, 10)
        self.assertEqual(updated_vertex.radius, 30)
        self.assertIsInstance(updated_vertex.properties, list)
        self.assertEqual(len(updated_vertex.properties), 0)
        self.assertEqual(len(self.graph.vertices), 2)

    def test_with_new_properties(self):
        # Arrange
        new_vertex = Vertex(
            _id='',
            name='Surgery',
            position_x=10,
            position_y=10,
            radius=30,
            properties=[
                Property(key='type', required=True, datatype=Datatype.STRING),
                Property(key='difficulty', required=False, datatype=Datatype.INT)
            ]
        )

        # Act
        self.graph.update_vertex(self.hobby_vertex_id, new_vertex)

        # Assert
        updated_vertex = self.graph.find_vertex_by_id(self.hobby_vertex_id)
        self.assertEqual(updated_vertex.id, self.hobby_vertex_id)
        self.assertEqual(updated_vertex.name, 'Surgery')
        self.assertEqual(updated_vertex.position_x, 10)
        self.assertEqual(updated_vertex.position_y, 10)
        self.assertEqual(updated_vertex.radius, 30)
        self.assertIsInstance(updated_vertex.properties, list)
        self.assertEqual(len(updated_vertex.properties), 2)
        self.assertEqual(updated_vertex.properties[0].key, 'type')
        self.assertEqual(updated_vertex.properties[0].required, True)
        self.assertEqual(updated_vertex.properties[0].datatype, 'String')
        self.assertEqual(updated_vertex.properties[1].key, 'difficulty')
        self.assertEqual(updated_vertex.properties[1].required, False)
        self.assertEqual(updated_vertex.properties[1].datatype, 'Int')
        self.assertEqual(len(self.graph.vertices), 2)


class TestGraphDeleteVertex(unittest.TestCase):
    def setUp(self):
        # Vertices
        self.person_vertex_id = str(uuid.uuid4())
        self.person_vertex = Vertex(
            _id=self.person_vertex_id,
            name='Person',
            position_x=0,
            position_y=0,
            radius=20,
            properties=[Property(key='name', required=True, datatype=Datatype.STRING)]
        )
        self.hobby_vertex_id = str(uuid.uuid4())
        self.hobby_vertex = Vertex(
            _id=self.hobby_vertex_id,
            name='Hobby',
            position_x=0,
            position_y=0,
            radius=20,
            properties=[]
        )
        # Edge
        self.performs_edge_id = str(uuid.uuid4())
        self.performs_edge = Edge(
            _id=self.performs_edge_id,
            name='performs',
            properties=[],
            multi_edge=True
        )
        self.likes_edge_id = str(uuid.uuid4())
        self.likes_edge = Edge(
            _id=self.likes_edge_id,
            name='likes',
            properties=[Property(key='strength', required=True, datatype=Datatype.FLOAT)],
            multi_edge=True
        )
        # Build Graph
        self.graph = Graph()
        self.graph.add_vertex(self.person_vertex)
        self.graph.add_vertex(self.hobby_vertex)
        self.graph.add_edge(self.performs_edge, self.person_vertex_id, self.hobby_vertex_id)
        self.graph.add_edge(self.likes_edge, self.person_vertex_id, self.person_vertex_id)

    def test_with_invalid_vertex_id(self):
        # Act
        with self.assertRaises(VertexNotFoundException) as context:
            self.graph.delete_vertex('invalid-id')

        # Assert
        self.assertEqual(context.exception.message, "Vertex with Id 'invalid-id' not found")
        self.assertEqual(len(self.graph.vertices), 2)
        self.assertEqual(len(self.graph.edges), 2)

    def test_delete_ordinary_connected_vertex(self):
        # Act
        self.graph.delete_vertex(self.hobby_vertex_id)

        # Assert
        self.assertEqual(len(self.graph.vertices), 1)
        self.assertEqual(self.graph.vertices[0], self.person_vertex)
        self.assertEqual(len(self.graph.edges), 1)
        self.assertEqual(self.graph.edges[0], self.likes_edge)

        self.assertEqual(len(self.graph.vertices[0].out_edges), 1)
        self.assertEqual(len(self.graph.vertices[0].in_edges), 1)

    def test_delete_recursive_connected_vertex(self):
        # Act
        self.graph.delete_vertex(self.person_vertex_id)

        # Assert
        self.assertEqual(len(self.graph.vertices), 1)
        self.assertEqual(self.graph.vertices[0], self.hobby_vertex)
        self.assertEqual(len(self.graph.edges), 0)

        self.assertEqual(len(self.graph.vertices[0].out_edges), 0)
        self.assertEqual(len(self.graph.vertices[0].in_edges), 0)


class TestGraphFindEdgeById(unittest.TestCase):
    def setUp(self):
        self.vertex_id = str(uuid.uuid4())
        vertex = Vertex(
            _id=self.vertex_id,
            name='TestVertex',
            position_x=0,
            position_y=0,
            radius=20,
            properties=[],
        )

        self.edge_id = str(uuid.uuid4())
        self.edge = Edge(
            _id=self.edge_id,
            name='Edge1',
            properties=[],
            multi_edge=True
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
            properties=[],
            multi_edge=True
        )

        # Act
        self.graph.add_edge(performs_edge, self.person_vertex_id, self.hobby_vertex_id)

        # Assert
        new_edge = self.graph.find_edge_by_id(performs_edge_id)
        self.assertEqual(id(new_edge), id(performs_edge))
        self.assertEqual(id(new_edge.source_vertex), id(self.person_vertex))
        self.assertEqual(id(new_edge.target_vertex), id(self.hobby_vertex))
        self.assertEqual(len(self.graph.edges), 1)
        self.assertEqual(len(self.person_vertex.out_edges), 1)
        self.assertEqual(len(self.person_vertex.in_edges), 0)
        self.assertEqual(len(self.hobby_vertex.out_edges), 0)
        self.assertEqual(len(self.hobby_vertex.in_edges), 1)
        self.assertEqual(new_edge.multi_edge, True)

    def test_new_edge_recursive(self):
        # Arrange
        likes_edge_id = str(uuid.uuid4())
        likes_edge = Edge(
            _id=likes_edge_id,
            name='likes',
            properties=[],
            multi_edge=False
        )

        # Act
        self.graph.add_edge(likes_edge, self.person_vertex_id, self.person_vertex_id)

        new_edge = self.graph.find_edge_by_id(likes_edge_id)
        self.assertEqual(id(new_edge), id(likes_edge))
        self.assertEqual(id(new_edge.source_vertex), id(self.person_vertex))
        self.assertEqual(id(new_edge.target_vertex), id(self.person_vertex))
        self.assertEqual(id(new_edge.source_vertex), id(new_edge.target_vertex))
        self.assertEqual(len(self.graph.edges), 1)
        self.assertEqual(len(self.person_vertex.out_edges), 1)
        self.assertEqual(len(self.person_vertex.in_edges), 1)
        self.assertEqual(len(self.hobby_vertex.out_edges), 0)
        self.assertEqual(len(self.hobby_vertex.in_edges), 0)
        self.assertEqual(new_edge.multi_edge, False)


class TestGraphUpdateEdge(unittest.TestCase):
    def setUp(self):
        # Vertices
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
        # Edges
        self.performs_edge_id = str(uuid.uuid4())
        self.performs_edge = Edge(
            _id=self.performs_edge_id,
            name='performs',
            properties=[],
            multi_edge=True
        )
        self.likes_edge_id = str(uuid.uuid4())
        self.likes_edge = Edge(
            _id=self.likes_edge_id,
            name='likes',
            properties=[],
            multi_edge=True
        )
        self.new_edge = Edge(
            _id='',
            name='new',
            properties=[],
            multi_edge=True
        )
        # Build Graph
        self.graph = Graph()
        self.graph.add_vertex(self.person_vertex)
        self.graph.add_vertex(self.hobby_vertex)
        self.graph.add_edge(self.performs_edge, self.person_vertex_id, self.hobby_vertex_id)
        self.graph.add_edge(self.likes_edge, self.person_vertex_id, self.person_vertex_id)

    def test_invalid_edge_id(self):
        # Act
        with self.assertRaises(EdgeNotFoundException) as context:
            self.graph.update_edge('invalid_id', self.person_vertex_id, self.hobby_vertex_id, self.new_edge)

        # Assert
        self.assertEqual(context.exception.message, "Edge with Id 'invalid_id' not found")
        self.assertEqual(len(self.graph.edges), 2)

    def test_update_attributes(self):
        # Arrange
        edge_with_attributes = Edge(
            _id='',
            name='likes_new',
            properties=[
                Property(key='strength', required=True, datatype=Datatype.FLOAT)
            ],
            multi_edge=False
        )

        # Act
        self.graph.update_edge(self.likes_edge_id, self.person_vertex_id, self.person_vertex_id, edge_with_attributes)

        # Assert
        self.assertEqual(self.graph.edges[1].id, self.likes_edge_id)
        self.assertEqual(self.graph.edges[1].name, 'likes_new')
        self.assertEqual(self.graph.edges[1].properties[0].key, 'strength')
        self.assertEqual(self.graph.edges[1].properties[0].required, True)
        self.assertEqual(self.graph.edges[1].properties[0].datatype, 'Float')
        self.assertEqual(self.graph.edges[1].multi_edge, False)

    def test_recursive_edge_with_duplicate_name(self):
        # Arrange
        duplicate_edge = Edge(
            _id='',
            name='performs',
            properties=[],
            multi_edge=False
        )

        # Act
        with self.assertRaises(EdgeException) as context:
            self.graph.update_edge(self.likes_edge_id, self.person_vertex_id, self.person_vertex_id, duplicate_edge)

        # Assert
        self.assertEqual(context.exception.message, "Source-Vertex already has an outgoing edge with name 'performs'")
        self.assertEqual(len(self.graph.edges), 2)

    def test_ordinary_edge_with_duplicate_name(self):
        # Arrange
        duplicate_edge = Edge(
            _id='',
            name='likes',
            properties=[],
            multi_edge=True
        )

        # Act
        with self.assertRaises(EdgeException) as context:
            self.graph.update_edge(self.performs_edge_id, self.person_vertex_id, self.hobby_vertex_id, duplicate_edge)

        # Assert
        self.assertEqual(context.exception.message, "Source-Vertex already has an outgoing edge with name 'likes'")
        self.assertEqual(len(self.graph.edges), 2)

    def test_update_ordinary_edge(self):
        # Act
        self.graph.update_edge(self.performs_edge_id, self.person_vertex_id, self.hobby_vertex_id, self.new_edge)

        # Assert
        self.assertEqual(len(self.graph.edges), 2)
        self.assertEqual(self.graph.edges[0].id, self.performs_edge_id)
        self.assertEqual(self.graph.edges[1].id, self.likes_edge_id)

        self.assertEqual(len(self.graph.vertices[0].out_edges), 2)
        self.assertEqual(self.graph.vertices[0].out_edges[0].id, self.likes_edge_id)
        self.assertEqual(self.graph.vertices[0].out_edges[1].id, self.performs_edge_id)
        self.assertEqual(self.graph.vertices[0].out_edges[1].name, 'new')

        self.assertEqual(len(self.graph.vertices[0].in_edges), 1)
        self.assertEqual(self.graph.vertices[0].in_edges[0].id, self.likes_edge_id)

        self.assertEqual(len(self.graph.vertices[1].out_edges), 0)

        self.assertEqual(len(self.graph.vertices[1].in_edges), 1)
        self.assertEqual(self.graph.vertices[1].in_edges[0].id, self.performs_edge_id)
        self.assertEqual(self.graph.vertices[1].in_edges[0].name, 'new')

    def test_update_recursive_edge(self):
        # Act
        self.graph.update_edge(self.likes_edge_id, self.person_vertex_id, self.person_vertex_id, self.new_edge)

        # Assert
        self.assertEqual(len(self.graph.edges), 2)
        self.assertEqual(self.graph.edges[0].id, self.performs_edge_id)
        self.assertEqual(self.graph.edges[1].id, self.likes_edge_id)

        self.assertEqual(len(self.graph.vertices[0].out_edges), 2)
        self.assertEqual(self.graph.vertices[0].out_edges[0].id, self.performs_edge_id)
        self.assertEqual(self.graph.vertices[0].out_edges[1].id, self.likes_edge_id)
        self.assertEqual(self.graph.vertices[0].out_edges[1].name, 'new')

        self.assertEqual(len(self.graph.vertices[0].in_edges), 1)
        self.assertEqual(self.graph.vertices[0].in_edges[0].id, self.likes_edge_id)
        self.assertEqual(self.graph.vertices[0].in_edges[0].name, 'new')

        self.assertEqual(len(self.graph.vertices[1].out_edges), 0)

        self.assertEqual(len(self.graph.vertices[1].in_edges), 1)
        self.assertEqual(self.graph.vertices[1].in_edges[0].id, self.performs_edge_id)

    def test_redirect_edge_from_ordinary_to_recursive(self):
        # Act
        self.graph.update_edge(self.performs_edge_id, self.person_vertex_id, self.person_vertex_id, self.performs_edge)

        # Assert
        self.assertEqual(len(self.graph.edges), 2)
        self.assertEqual(self.graph.edges[0].id, self.performs_edge_id)
        self.assertEqual(self.graph.edges[1].id, self.likes_edge_id)

        self.assertEqual(len(self.graph.vertices[0].out_edges), 2)
        self.assertEqual(self.graph.vertices[0].out_edges[0].id, self.likes_edge_id)
        self.assertEqual(self.graph.vertices[0].out_edges[1].id, self.performs_edge_id)

        self.assertEqual(len(self.graph.vertices[0].in_edges), 2)
        self.assertEqual(self.graph.vertices[0].in_edges[0].id, self.likes_edge_id)
        self.assertEqual(self.graph.vertices[0].in_edges[1].id, self.performs_edge_id)

        self.assertEqual(len(self.graph.vertices[1].out_edges), 0)

        self.assertEqual(len(self.graph.vertices[1].in_edges), 0)

    def test_redirect_edge_from_recursive_to_ordinary(self):
        # Act
        self.graph.update_edge(self.likes_edge_id, self.person_vertex_id, self.hobby_vertex_id, self.likes_edge)

        # Assert
        self.assertEqual(len(self.graph.edges), 2)
        self.assertEqual(self.graph.edges[0].id, self.performs_edge_id)
        self.assertEqual(self.graph.edges[1].id, self.likes_edge_id)

        self.assertEqual(len(self.graph.vertices[0].out_edges), 2)
        self.assertEqual(self.graph.vertices[0].out_edges[0].id, self.performs_edge_id)
        self.assertEqual(self.graph.vertices[0].out_edges[1].id, self.likes_edge_id)

        self.assertEqual(len(self.graph.vertices[0].in_edges), 0)

        self.assertEqual(len(self.graph.vertices[1].out_edges), 0)

        self.assertEqual(len(self.graph.vertices[1].in_edges), 2)
        self.assertEqual(self.graph.vertices[1].in_edges[0].id, self.performs_edge_id)
        self.assertEqual(self.graph.vertices[1].in_edges[1].id, self.likes_edge_id)

    def test_turn_around_edge(self):
        # Act
        self.graph.update_edge(self.performs_edge_id, self.hobby_vertex_id, self.person_vertex_id, self.performs_edge)

        # Assert
        self.assertEqual(len(self.graph.edges), 2)
        self.assertEqual(self.graph.edges[0].id, self.performs_edge_id)
        self.assertEqual(self.graph.edges[1].id, self.likes_edge_id)

        self.assertEqual(len(self.graph.vertices[0].out_edges), 1)
        self.assertEqual(self.graph.vertices[0].out_edges[0].id, self.likes_edge_id)

        self.assertEqual(len(self.graph.vertices[0].in_edges), 2)
        self.assertEqual(self.graph.vertices[0].in_edges[0].id, self.likes_edge_id)
        self.assertEqual(self.graph.vertices[0].in_edges[1].id, self.performs_edge_id)

        self.assertEqual(len(self.graph.vertices[1].out_edges), 1)
        self.assertEqual(self.graph.vertices[1].out_edges[0].id, self.performs_edge_id)

        self.assertEqual(len(self.graph.vertices[1].in_edges), 0)

    def test_redirect_ordinary_edge_to_recursive_with_duplicate_name(self):
        # Act
        with self.assertRaises(EdgeException) as context:
            self.graph.update_edge(self.performs_edge_id, self.person_vertex_id, self.person_vertex_id, self.likes_edge)

        # Assert
        self.assertEqual(context.exception.message, "Source-Vertex already has an outgoing edge with name 'likes'")
        self.assertEqual(len(self.graph.edges), 2)

    def test_redirect_recursive_edge_to_ordinary_with_duplicate_name(self):
        # Act
        with self.assertRaises(EdgeException) as context:
            self.graph.update_edge(self.likes_edge_id, self.person_vertex_id, self.hobby_vertex_id, self.performs_edge)

        # Assert
        self.assertEqual(context.exception.message, "Source-Vertex already has an outgoing edge with name 'performs'")
        self.assertEqual(len(self.graph.edges), 2)


class TestGraphDeleteEdge(unittest.TestCase):
    def setUp(self):
        # Vertices
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
        # Edges
        self.performs_edge_id = str(uuid.uuid4())
        self.performs_edge = Edge(
            _id=self.performs_edge_id,
            name='performs',
            properties=[],
            multi_edge=True
        )
        self.likes_edge_id = str(uuid.uuid4())
        self.likes_edge = Edge(
            _id=self.likes_edge_id,
            name='likes',
            properties=[],
            multi_edge=True
        )
        # Build Graph
        self.graph = Graph()
        self.graph.add_vertex(self.person_vertex)
        self.graph.add_vertex(self.hobby_vertex)
        self.graph.add_edge(self.performs_edge, self.person_vertex_id, self.hobby_vertex_id)
        self.graph.add_edge(self.likes_edge, self.person_vertex_id, self.person_vertex_id)

    def test_invalid_edge_id(self):
        # Act
        with self.assertRaises(EdgeNotFoundException) as context:
            self.graph.delete_edge('invalid_id')

        # Assert
        self.assertEqual(context.exception.message, "Edge with Id 'invalid_id' not found")

    def test_delete_ordinary_edge(self):
        # Act
        self.graph.delete_edge(self.performs_edge_id)

        # Assert
        self.assertEqual(len(self.graph.edges), 1)
        self.assertEqual(self.graph.edges[0].id, self.likes_edge_id)

        self.assertEqual(len(self.person_vertex.out_edges), 1)
        self.assertEqual(self.person_vertex.out_edges[0].id, self.likes_edge_id)

        self.assertEqual(len(self.person_vertex.in_edges), 1)
        self.assertEqual(self.person_vertex.in_edges[0].id, self.likes_edge_id)

        self.assertEqual(len(self.hobby_vertex.out_edges), 0)

        self.assertEqual(len(self.hobby_vertex.in_edges), 0)

    def test_delete_recursive_edge(self):
        # Act
        self.graph.delete_edge(self.likes_edge_id)

        # Assert
        self.assertEqual(len(self.graph.edges), 1)
        self.assertEqual(self.graph.edges[0].id, self.performs_edge_id)

        self.assertEqual(len(self.person_vertex.out_edges), 1)
        self.assertEqual(self.person_vertex.out_edges[0].id, self.performs_edge_id)

        self.assertEqual(len(self.person_vertex.in_edges), 0)

        self.assertEqual(len(self.hobby_vertex.out_edges), 0)

        self.assertEqual(len(self.hobby_vertex.in_edges), 1)
        self.assertEqual(self.hobby_vertex.in_edges[0].id, self.performs_edge_id)
