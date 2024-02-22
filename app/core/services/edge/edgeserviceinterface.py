from abc import ABC, abstractmethod
from typing import List

from app.core.entities import Edge


class IEdgeService(ABC):
    @abstractmethod
    def get_edges(self, project_id: str) -> List[Edge]:
        pass

    @abstractmethod
    def get_edge(self, project_id: str, edge_id: str) -> Edge:
        pass

    @abstractmethod
    def create_edge(self, project_id: str, edge: Edge, source_vertex_id: str, target_vertex_id: str) -> Edge:
        pass

    @abstractmethod
    def update_edge(
            self,
            project_id: str,
            edge_id: str,
            source_vertex_id: str,
            target_vertex_id: str,
            edge: Edge
    ) -> Edge:
        pass

    @abstractmethod
    def delete_edge(self, project_id: str, edge_id: str):
        pass
