from typing import List
from app.core.repositories import IVertexRepository
from app.core.services import IVertexService
from app.core.entities import Vertex


class VertexService(IVertexService):
    def __init__(self, repository: IVertexRepository):
        self.repository = repository

    def get_vertices(self) -> List[Vertex]:
        vertices = self.repository.get_vertices()

        return vertices

    def create_vertex(self, vertex: Vertex) -> Vertex:
        vertex = self.repository.create_vertex(vertex)

        return vertex
