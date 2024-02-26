from graph.vertex import Vertex


class Graph:
    def __init__(self):
        self.vertices = []
        self.edges = []

    def find_vertex_by_id(self, vertex_id) -> Vertex:
        for vertex in self.vertices:
            if vertex.id == vertex_id:
                return vertex

        raise Exception(f"Vertex with Id '{vertex_id}' not found")

    def find_edge_by_id(self, edge_id) -> Vertex:
        for edge in self.edges:
            if edge.id == edge_id:
                return edge

        raise Exception(f"Edge with Id '{edge_id}' not found")
