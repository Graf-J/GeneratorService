from abc import ABC, abstractmethod
from typing import List

from app.core.entities import Vertex


class IVertexRepository(ABC):
    @abstractmethod
    def get_vertices(self, project_id: str) -> List[Vertex]:
        pass

    @abstractmethod
    def get_vertex(self, project_id: str, vertex_id: str) -> Vertex:
        pass

    @abstractmethod
    def create_vertex(self, project_id: str, vertex: Vertex) -> Vertex:
        pass
