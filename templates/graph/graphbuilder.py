from graph.graph import Graph
from graph.vertex import Vertex
from graph.edge import Edge


class GraphBuilder:
    def __init__(self):
        self.graph = Graph()

    def add_vertex(self, vertex: Vertex):
        self.graph.vertices.append(vertex)

        return self

    def add_edge(self, edge: Edge):
        # Find Vertices
        source_vertex = self.graph.find_vertex_by_id(edge.source_vertex_id)
        target_vertex = self.graph.find_vertex_by_id(edge.target_vertex_id)

        # Set Vertices of Edge
        edge.source_vertex = source_vertex
        edge.target_vertex = target_vertex

        # Append Edge to Vertices
        source_vertex.out_edges.append(edge)
        target_vertex.in_edges.append(edge)

        # Append Edge to Graph
        self.graph.edges.append(edge)

        return self

    def build(self):
        return self.graph
