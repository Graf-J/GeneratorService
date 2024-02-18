from abc import ABC, abstractmethod
from typing import List
from app.core.entities import Vertex


class IVertexRepository(ABC):
    @abstractmethod
    def get_vertices(self) -> List[Vertex]:
        pass

    def create_vertex(self, vertex: Vertex) -> Vertex:
        pass
