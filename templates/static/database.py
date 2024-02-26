from gremlin_python.driver.aiohttp.transport import AiohttpTransport
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.driver.protocol import GremlinServerError
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import __
from gremlin_python.structure.io import graphsonV3d0


class GraphDatabase:
    def __init__(self, pool_size=5):
        uri = f'ws://localhost:8182/gremlin'
        self.connection_manager = DriverRemoteConnection(
            uri,
            pool_size=pool_size,
            transport_factory=lambda: AiohttpTransport(call_from_event_loop=True),
            graphson_reader=graphsonV3d0.GraphSONReader(),
            graphson_writer=graphsonV3d0.GraphSONWriter()
        )

    @property
    def g(self):
        return traversal().withRemote(self.connection)

    def vertex_with_label_exists(self, vertex_id, label):
        return self.g.V(vertex_id).hasLabel(label).hasNext()

    def vertex_exists(self, vertex_id):
        return self.g.V(vertex_id).hasNext()

    def edge_with_label_between_vertices_with_label_exists(self, edge_id, edge_label, source_vertex_label,
                                                           target_vertex_label):
        try:
            return self.g.V().hasLabel(source_vertex_label).outE(edge_label).has_id(edge_id).inV().hasLabel(
                target_vertex_label).hasNext()
        except GremlinServerError:
            return False

    def edge_exists(self, edge_id):
        try:
            return self.g.E(edge_id).hasNext()
        except GremlinServerError:
            return False

    def add_vertex(self, label, properties):
        # Add Label
        g = self.g.addV(label)
        # Add Properties
        for key, value in properties.items():
            g = g.property(key, value)
        # Execute Query
        vertex = g.next()

        return vertex.id

    def add_vertex_empty(self, label):
        # Execute Query
        vertex = self.g.addV(label).next()

        return vertex.id

    def update_vertex(self, vertex_id, data, property_field_names):
        # Get Vertex By ID
        g = self.g.V(vertex_id)
        # Add Properties
        for property_field_name in property_field_names:
            g = g.property(property_field_name, data.get(property_field_name))
        # Execute Query
        vertex = g.next()

        return vertex.id

    def delete_vertex(self, vertex_id):
        self.g.V(vertex_id).drop().iterate()

    def connect_vertices(self, source_vertex_id, target_vertex_id, label, data, *, multi_edge):
        # Check for Multi-Edge condition
        if not multi_edge:
            count = self.g.V(source_vertex_id).outE().hasLabel(label).where(
                __.in_v().has_id(target_vertex_id)
            ).count().next()
            if count > 0:
                raise Exception(
                    f"From Vertex with ID {source_vertex_id} to Vertex with ID {target_vertex_id} a edge with Label '{label}' already exists")

        # Build Query
        g = self.g.V(source_vertex_id).as_('source').V(target_vertex_id).as_('target').addE(label).from_('source').to(
            'target')
        for key, value in data.items():
            g = g.property(key, value)
        # Execute Query
        edge = g.next()

        return edge.id

    def connect_vertices_empty(self, source_vertex_id, target_vertex_id, label, *, multi_edge):
        # Check for Multi-Edge condition
        if not multi_edge:
            count = self.g.V(source_vertex_id).outE().hasLabel(label).where(
                __.in_v().has_id(target_vertex_id)
            ).count().next()
            if count > 0:
                raise Exception(
                    f"From Vertex with ID '{source_vertex_id}' to Vertex with ID '{target_vertex_id}' a edge with Label '{label}' already exists")

        # Execute Query
        edge = self.g.V(source_vertex_id).as_('source').V(target_vertex_id).as_('target').addE(label).from_(
            'source').to(
            'target').next()

        return edge.id

    def update_edge(self, edge_id, data, property_field_names):
        # Get Vertex By ID
        g = self.g.E(edge_id)
        # Add Properties
        for property_field_name in property_field_names:
            g = g.property(property_field_name, data.get(property_field_name))
        # Execute Query
        edge = g.next()

        return edge.id

    def delete_edge(self, edge_id):
        self.g.E(edge_id).drop().iterate()

    def __enter__(self):
        self.connection = self.connection_manager
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass

    def close(self):
        self.connection_manager.close()
