from typing import List

from app.core.entities.edge import Edge
from app.core.entities.vertex import Vertex
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
        vertex.properties = new_vertex.properties

        return vertex

    def delete_vertex(self, vertex_id: str):
        vertex = self.find_vertex_by_id(vertex_id)

        # Delete Edge from Target-Vertex's In-Edges + Delete Edge from Graph
        for edge in vertex.out_edges:
            edge.target_vertex.in_edges.remove(edge)
            self.edges.remove(edge)

        # Delete Edge from Source-Vertex's Out-Edges + Delete Edge from Graph
        # Hint: In case of recursion the in_edge already got removed in the loop above, so no duplicate deletion
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
        EdgeValidator.validate_edge_properties(
            edge,
            source_vertex,
            target_vertex
        )
        EdgeValidator.validate_connected_vertices_connections(
            edge,
            source_vertex.out_edges,
            target_vertex.in_edges
        )
        EdgeValidator.validate_connected_vertices_properties(
            edge,
            source_vertex.properties,
            target_vertex.properties
        )

        # Set values of Vertices
        source_vertex.add_out_edge(edge)
        target_vertex.add_in_edge(edge)

        # Set values of Edge
        edge.source_vertex = source_vertex
        edge.target_vertex = target_vertex

        self.edges.append(edge)

    def update_edge(self, edge_id: str, source_vertex_id: str, target_vertex_id: str, new_edge: Edge) -> Edge:
        # Get Data
        source_vertex = self.find_vertex_by_id(source_vertex_id)
        target_vertex = self.find_vertex_by_id(target_vertex_id)
        edge = self.find_edge_by_id(edge_id)

        # Validate Edge
        source_vertex_out_edges_without_new_edge = list(filter(lambda e: e != edge, source_vertex.out_edges))
        target_vertex_in_edges_without_new_edge = list(filter(lambda e: e != edge, target_vertex.in_edges))
        EdgeValidator.validate_edge_properties(
            new_edge,
            source_vertex,
            target_vertex
        )
        EdgeValidator.validate_connected_vertices_connections(
            new_edge,
            source_vertex_out_edges_without_new_edge,
            target_vertex_in_edges_without_new_edge
        )
        EdgeValidator.validate_connected_vertices_properties(
            new_edge,
            source_vertex.properties,
            target_vertex.properties
        )

        # Set Attributes of Edge
        edge.name = new_edge.name
        edge.properties = new_edge.properties
        edge.multi_edge = new_edge.multi_edge
        # Disconnect Edge from previous Vertices
        edge.source_vertex.out_edges.remove(edge)
        edge.target_vertex.in_edges.remove(edge)
        # Connect Edge to new Vertices
        source_vertex.add_out_edge(edge)
        target_vertex.add_in_edge(edge)
        # Set Vertices of Edge
        edge.source_vertex = source_vertex
        edge.target_vertex = target_vertex

        return edge

    def delete_edge(self, edge_id: str):
        edge = self.find_edge_by_id(edge_id)

        edge.source_vertex.out_edges.remove(edge)
        edge.target_vertex.in_edges.remove(edge)
        self.edges.remove(edge)

    #########
    # Other #
    #########
    def to_dict(self) -> dict:
        return {
            'vertices': [vertex.to_dict() for vertex in self.vertices],
            'edges': [edge.to_dict() for edge in self.edges]
        }
