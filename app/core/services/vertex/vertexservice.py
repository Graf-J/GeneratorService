from typing import List

from app.core.entities import Vertex
from app.core.repositories import IVertexRepository
from app.core.services.vertex.vertexserviceinterface import IVertexService


class VertexService(IVertexService):
    def __init__(self, repository: IVertexRepository):
        self.repository = repository

    def get_vertices(self, project_id: str) -> List[Vertex]:
        vertices = self.repository.get_vertices(project_id)

        return vertices

    def get_vertex(self, project_id: str, vertex_id: str) -> Vertex:
        vertex = self.repository.get_vertex(project_id, vertex_id)

        return vertex

    def create_vertex(self, project_id: str, vertex: Vertex) -> Vertex:
        vertex = self.repository.create_vertex(project_id, vertex)

        return vertex
