from typing import List

from app.core.entities import Vertex, Edge, Property
from app.core.exceptions import EdgeException


class EdgeValidator:
    @staticmethod
    def validate_connected_vertices_connections(
            new_edge: Edge,
            source_vertex_out_edges: List[Edge],
            target_vertex_in_edges: List[Edge]
    ):
        # Check if Source-Vertex already has outgoing Edge with this name
        for edge in source_vertex_out_edges:
            if new_edge.name_lower == edge.name_lower:
                raise EdgeException(f"Source-Vertex already has an outgoing edge with name '{edge.name}'")

        # Check if Target-Vertex already has incoming Edge with this name
        for edge in target_vertex_in_edges:
            if new_edge.name_lower == edge.name_lower:
                raise EdgeException(f"Target-Vertex already has an incoming edge with name '{edge.name}'")

    @staticmethod
    def validate_connected_vertices_properties(
            new_edge: Edge,
            source_vertex_properties: List[Property],
            target_vertex_properties: List[Property]
    ):
        # Check if Properties of Source Vertex got Conflicts with new Edge name
        for prop in source_vertex_properties:
            if new_edge.out_field_name == prop.key:
                raise EdgeException(f"Edge name has conflict with property '{prop.key}' of Source-Vertex")

        # Check if Properties of Target Vertex got Conflicts with new Edge name
        for prop in target_vertex_properties:
            if new_edge.in_field_name == prop.key:
                raise EdgeException(f"Edge name has conflict with property '{prop.key}' of Target-Vertex")

    @staticmethod
    def validate_edge_properties(new_edge: Edge, source_vertex: Vertex, target_vertex: Vertex):
        for prop in new_edge.properties:
            if prop.key == source_vertex.name_lower:
                raise EdgeException(f"Edge property '{prop.key}' has conflict with Source-Vertex")

            if prop.key == target_vertex.name_lower:
                raise EdgeException(f"Edge property '{prop.key}' has conflict with Target-Vertex")
