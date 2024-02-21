from typing import List

from app.core.entities import Vertex, Edge
from app.core.exceptions import VertexNotFoundException, EdgeNotFoundException
from app.core.validators import VertexValidator, EdgeValidator


class Graph:
    def __init__(self):
        self.vertices: List[Vertex] = []
        self.edges: List[Edge] = []

    #####################
    # Vertex Operations #
    #####################
    def find_vertex_by_id(self, vertex_id: str) -> Vertex:
        for vertex in self.vertices:
            if vertex.id == vertex_id:
                return vertex

        raise VertexNotFoundException(f"Vertex with Id '{vertex_id}' not found")

    def add_vertex(self, vertex: Vertex):
        VertexValidator.validate_new_vertex(self.vertices, vertex)

        self.vertices.append(vertex)

    def update_vertex(self, vertex_id: str, new_vertex: Vertex) -> Vertex:
        # Find existing Vertex
        vertex = self.find_vertex_by_id(vertex_id)
        new_vertex.id = vertex_id

        # Validate new Vertex
        vertices_without_new_vertex = list(filter(lambda v: v.id != vertex_id, self.vertices))
        VertexValidator.validate_new_vertex(vertices_without_new_vertex, new_vertex)

        # Update Values
        vertex.name = new_vertex.name
        vertex.position_x = new_vertex.position_x
        vertex.position_y = new_vertex.position_y
        vertex.radius = new_vertex.radius
        vertex.properties = new_vertex.properties

        return vertex

    def delete_vertex(self, vertex_id: str):
        vertex = self.find_vertex_by_id(vertex_id)

        # Delete Edge from Target-Vertex the Edge points to and the Graph
        for edge in vertex.out_edges:
            edge.target_vertex.in_edges.remove(edge)
            self.edges.remove(edge)

        # Delete Edge from Source-Vertex the Edge comes from and the Graph
        # Hint: In case of recursion the in_edge already got removed in the loop above
        for edge in vertex.in_edges:
            edge.source_vertex.out_edges.remove(edge)
            self.edges.remove(edge)

        # Deletes the Vertex from the Graph and therefore all its Edges
        self.vertices.remove(vertex)

    ###################
    # Edge Operations #
    ###################
    def find_edge_by_id(self, edge_id: str) -> Edge:
        for edge in self.edges:
            if edge.id == edge_id:
                return edge

        raise EdgeNotFoundException(f"Edge with Id '{edge_id}' not found")

    def add_edge(self, edge: Edge, source_vertex_id: str, target_vertex_id: str):
        # Get Vertices which get connected through Edge
        source_vertex = self.find_vertex_by_id(source_vertex_id)
        target_vertex = self.find_vertex_by_id(target_vertex_id)

        # Validate the Edge
        EdgeValidator.validate_new_edge(edge, source_vertex.out_edges, target_vertex.in_edges)

        # Set values of Vertices
        source_vertex.add_out_edge(edge)
        target_vertex.add_in_edge(edge)

        # Set values of Edge
        edge.source_vertex = source_vertex
        edge.target_vertex = target_vertex

        self.edges.append(edge)
