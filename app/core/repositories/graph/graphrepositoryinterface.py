from abc import ABC, abstractmethod

from app.core.entities import Graph


class IGraphRepository(ABC):
    @abstractmethod
    def get_graph(self, project_id: str) -> Graph:
        pass
