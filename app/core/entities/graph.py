from typing import List
from app.core.entities import Vertex, Edge
from app.core.validators import VertexValidator


class Graph:
    def __init__(self):
        self.vertices: List[Vertex] = []
        self.edges: List[Edge] = []

    def add_vertex(self, vertex: Vertex):
        VertexValidator.validate_new_vertex(self.vertices, vertex)

        self.vertices.append(vertex)
