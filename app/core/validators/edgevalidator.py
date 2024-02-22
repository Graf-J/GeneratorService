from typing import List

from app.core.entities import Edge, Property
from app.core.exceptions import EdgeException


class EdgeValidator:
    @staticmethod
    def validate_new_edge_name(
            new_edge_name: str,
            source_vertex_out_edges: List[Edge],
            target_vertex_in_edges: List[Edge]
    ):
        # Check if Source-Vertex already has outgoing Edge with this name
        for edge in source_vertex_out_edges:
            if edge.name == new_edge_name:
                raise EdgeException(
                    f"Vertex already has an outgoing edge with name '{edge.name}'")

        # Check if Target-Vertex already has incoming Edge with this name
        for edge in target_vertex_in_edges:
            if edge.name == new_edge_name:
                raise EdgeException(
                    f"Vertex already has an incoming edge with name '{edge.name}'")

    @staticmethod
    def validate_connected_vertices_properties(
            new_edge_name: str,
            source_vertex_properties: List[Property],
            target_vertex_properties: List[Property]
    ):
        # Check if Properties of Source Vertex got Conflicts with new Edge name
        out_edge_name = new_edge_name + 'Out'
        for prop in source_vertex_properties:
            if prop.key == out_edge_name:
                raise EdgeException(f"Edge name has conflict with property '{prop.key}' of source vertex")

        # Check if Properties of Target Vertex got Conflicts with new Edge name
        in_edge_name = new_edge_name + 'In'
        for prop in target_vertex_properties:
            if prop.key == in_edge_name:
                raise EdgeException(f"Edge name has conflict with property '{prop.key}' of target vertex")
