from typing import List

from app.core.entities import Vertex
from app.core.exceptions import VertexException


class VertexValidator:
    @staticmethod
    def validate_new_vertex(vertices: List[Vertex], new_vertex: Vertex):
        for vertex in vertices:
            if vertex.id == new_vertex.id:
                raise VertexException(f"Vertex with Id '{vertex.id}' already exists")
            if vertex.name == new_vertex.name:
                raise VertexException(f"Vertex with Name '{vertex.name}' already exists")
