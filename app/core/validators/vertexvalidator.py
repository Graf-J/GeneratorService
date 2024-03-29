from typing import List

from app.core.entities.vertex import Vertex
from app.core.exceptions import VertexException


class VertexValidator:
    @staticmethod
    def validate_new_vertex(vertices: List[Vertex], new_vertex: Vertex):
        # Validations which depend on existing Vertex-Names
        for vertex in vertices:
            if new_vertex.id == vertex.id:
                raise VertexException(f"Vertex with Id '{vertex.id}' already exists", status_code=409, loc='id')
            if new_vertex.name_upper == vertex.name_upper:
                raise VertexException(f"Vertex with Name '{vertex.name}' already exists", status_code=422, loc='name')
