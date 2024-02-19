from typing import List

from app.core.entities import Vertex
from app.core.repositories.vertex.vertexrepositoryinterface import IVertexRepository
from app.infrastructure.storage.storageinterface import IStorage


class VertexRepository(IVertexRepository):
    def __init__(self, storage: IStorage):
        self.storage = storage

    def get_vertices(self, project_id: str) -> List[Vertex]:
        graph = self.storage.load_graph(project_id)
        vertices = graph.vertices

        return vertices

    def get_vertex(self, project_id: str, vertex_id: str) -> Vertex:
        graph = self.storage.load_graph(project_id)
        vertex = graph.find_vertex_by_id(vertex_id)

        return vertex

    def create_vertex(self, project_id: str, vertex: Vertex) -> Vertex:
        graph = self.storage.load_graph(project_id)
        graph.add_vertex(vertex)
        self.storage.save_graph(project_id, graph)

        return vertex
