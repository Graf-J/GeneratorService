from abc import ABC, abstractmethod
from typing import List
from app.core.entities import Vertex


class IVertexService(ABC):
    @abstractmethod
    def get_vertices(self) -> List[Vertex]:
        pass

    @abstractmethod
    def create_vertex(self, vertex: Vertex) -> Vertex:
        pass
