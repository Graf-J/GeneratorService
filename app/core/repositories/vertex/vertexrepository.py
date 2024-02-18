from typing import List
from app.core.entities import Vertex
from app.infrastructure.storage.storageinterface import IStorage
from app.core.repositories import IVertexRepository


class VertexRepository(IVertexRepository):
    def __init__(self, graph_storage: IStorage):
        self.graph_storage = graph_storage

    def get_vertices(self) -> List[Vertex]:
        pass

    def create_vertex(self, vertex: Vertex) -> Vertex:
        pass
