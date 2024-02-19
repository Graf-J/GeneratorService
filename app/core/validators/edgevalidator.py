from app.core.entities import Edge, Vertex
from app.core.exceptions import EdgeException


class EdgeValidator:
    @staticmethod
    def validate_new_edge(new_edge: Edge, source_vertex: Vertex, target_vertex: Vertex):
        # Check if Source-Vertex already has outgoing Edge with this name
        for edge in source_vertex.out_edges:
            if edge.name == new_edge.name:
                raise EdgeException(f'Vertex {source_vertex.name} already has an outgoing edge with name {edge.name}')

        # Check if Target-Vertex already has incoming Edge with this name
        for edge in target_vertex.in_edges:
            if edge.name == new_edge.name:
                raise EdgeException(f'Vertex {target_vertex.name} already has an incoming edge with name {edge.name}')
