from typing import List

from app.core.entities import Vertex
from app.core.exceptions import DuplicateException


class VertexValidator:
    @staticmethod
    def validate_new_vertex(vertices: List[Vertex], new_vertex: Vertex):
        for vertex in vertices:
            if vertex.id == new_vertex.id:
                raise DuplicateException('Vertex with Id already exists')
            if vertex.name == new_vertex.name:
                raise DuplicateException('Vertex with Name already exists')
