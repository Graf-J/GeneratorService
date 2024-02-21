from typing import List

from app.core.entities import Edge
from app.core.exceptions import EdgeException


class EdgeValidator:
    @staticmethod
    def validate_new_edge(new_edge: Edge, source_vertex_out_edges: List[Edge], target_vertex_in_edges: List[Edge]):
        # Check if Source-Vertex already has outgoing Edge with this name
        for edge in source_vertex_out_edges:
            if edge.name == new_edge.name:
                raise EdgeException(
                    f"Vertex already has an outgoing edge with name '{edge.name}'")

        # Check if Target-Vertex already has incoming Edge with this name
        for edge in target_vertex_in_edges:
            if edge.name == new_edge.name:
                raise EdgeException(
                    f"Vertex already has an incoming edge with name '{edge.name}'")
