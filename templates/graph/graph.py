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