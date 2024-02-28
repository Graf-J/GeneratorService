from gremlin_python.driver.aiohttp.transport import AiohttpTransport
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.driver.protocol import GremlinServerError
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import GraphTraversalSource
from gremlin_python.process.graph_traversal import __
from gremlin_python.structure.io import graphsonV3d0


class GraphDatabase:
    def __init__(self, pool_size=5):
        uri = 'ws://janusgraph:8182/gremlin'
        self.connection_manager = DriverRemoteConnection(
            uri,
            pool_size=pool_size,
            transport_factory=lambda: AiohttpTransport(call_from_event_loop=True),
            graphson_reader=graphsonV3d0.GraphSONReader(),
            graphson_writer=graphsonV3d0.GraphSONWriter()
        )

    @property
    def g(self) -> GraphTraversalSource:
        return traversal().withRemote(self.connection)

    def vertex_with_label_exists(self, vertex_id: str, label: str) -> bool:
        return self.g.V(vertex_id).has_label(label).has_next()

    def vertex_exists(self, vertex_id: str) -> bool:
        return self.g.V(vertex_id).has_next()

    def edge_with_label_between_vertices_with_label_exists(self, edge_id: str, edge_label: str,
                                                           source_vertex_label: str, target_vertex_label: str) -> bool:
        try:
            return self.g.V().has_label(source_vertex_label).outE(edge_label).has_id(edge_id).inV().has_label(
                target_vertex_label).has_next()
        except GremlinServerError:
            return False

    def edge_exists(self, edge_id: str) -> bool:
        try:
            return self.g.E(edge_id).has_next()
        except GremlinServerError:
            return False

    def add_vertex(self, label: str, properties: dict) -> str:
        # Add Label
        g = self.g.add_v(label)
        # Add Properties
        for key, value in properties.items():
            g = g.property(key, value)
        # Execute Query
        vertex = g.next()

        return vertex.id

    def add_vertex_empty(self, label: str) -> str:
        # Execute Query
        vertex = self.g.add_v(label).next()

        return vertex.id

    def update_vertex(self, vertex_id: str, data: dict, property_field_names: list) -> str:
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

    def connect_vertices(self, source_vertex_id: str, target_vertex_id: str, label: str, data: dict, *,
                         multi_edge: bool) -> str:
        # Check for Multi-Edge condition
        if not multi_edge:
            count = self.g.V(source_vertex_id).out_e().has_label(label).where(
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

    def connect_vertices_empty(self, source_vertex_id: str, target_vertex_id: str, label: str, *,
                               multi_edge: bool) -> str:
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

    def update_edge(self, edge_id: str, data: dict, property_field_names: list) -> str:
        # Get Vertex By ID
        g = self.g.E(edge_id)
        # Add Properties
        for property_field_name in property_field_names:
            g = g.property(property_field_name, data.get(property_field_name))
        # Execute Query
        edge = g.next()

        return edge.id

    def delete_edge(self, edge_id: str):
        self.g.E(edge_id).drop().iterate()

    def __enter__(self):
        self.connection = self.connection_manager
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass

    def close(self):
        self.connection_manager.close()
