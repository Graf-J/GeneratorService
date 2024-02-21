from typing import List

from app.core.entities import Vertex, Edge
from app.core.exceptions import VertexNotFoundException, EdgeNotFoundException
from app.core.validators import VertexValidator, EdgeValidator


class Graph:
    def __init__(self):
        self.vertices: List[Vertex] = []
        self.edges: List[Edge] = []

    def find_vertex_by_id(self, vertex_id: str) -> Vertex:
        for vertex in self.vertices:
            if vertex.id == vertex_id:
                return vertex

        raise VertexNotFoundException(f"Vertex with Id '{vertex_id}' not found")

    def find_edge_by_id(self, edge_id: str) -> Edge:
        for edge in self.edges:
            if edge.id == edge_id:
                return edge

        raise EdgeNotFoundException(f"Edge with Id '{edge_id}' not found")

    def add_vertex(self, vertex: Vertex):
        VertexValidator.validate_new_vertex(self.vertices, vertex)

        self.vertices.append(vertex)

    def add_edge(self, edge: Edge, source_vertex_id: str, target_vertex_id: str):
        # Get Vertices which get connected through Edge
        source_vertex = self.find_vertex_by_id(source_vertex_id)
        target_vertex = self.find_vertex_by_id(target_vertex_id)

        # Validate the Edge
        EdgeValidator.validate_new_edge(edge, source_vertex, target_vertex)

        # Set values of Vertices
        source_vertex.add_out_edge(edge)
        target_vertex.add_in_edge(edge)

        # Set values of Edge
        edge.source_vertex = source_vertex
        edge.target_vertex = target_vertex

        self.edges.append(edge)
