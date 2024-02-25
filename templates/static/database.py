from gremlin_python.driver.aiohttp.transport import AiohttpTransport
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.anonymous_traversal import traversal


class GraphDatabase:
    def __init__(self, pool_size=5):
        uri = f'ws://localhost:8182/gremlin'
        self.connection_manager = DriverRemoteConnection(
            uri, pool_size=pool_size, transport_factory=lambda: AiohttpTransport(call_from_event_loop=True))

    @property
    def g(self):
        return traversal().withRemote(self.connection)

    def vertex_exists(self, vertex_id, label):
        return self.g.V(vertex_id).hasLabel(label).hasNext()

    def add_vertex(self, label, properties):
        # Add Label
        g = self.g.addV(label)
        # Add Properties
        for key, value in properties.items():
            g = g.property(key, value)
        # Execute Query
        vertex = g.next()

        return vertex.id

    def add_empty_vertex(self, label):
        # Add empty Vertex
        g = self.g.addV(label)
        # Execute Query
        vertex = g.next()

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
        res = self.g.V(vertex_id).drop().iterate()
        print(res)

    def __enter__(self):
        self.connection = self.connection_manager
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass

    def close(self):
        self.connection_manager.close()
