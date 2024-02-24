from abc import ABC, abstractmethod
from typing import List

from app.core.entities import Graph, Project


class IProjectStorage(ABC):
    @abstractmethod
    def get_projects(self) -> List[Project]:
        pass

    @abstractmethod
    def get_project(self, project_id: str) -> Project:
        pass

    @abstractmethod
    def create_project(self, project: Project) -> Project:
        pass

    @abstractmethod
    def delete_project(self, project_id: str):
        pass

    @abstractmethod
    def load_graph(self, project_id: str) -> Graph:
        pass

    @abstractmethod
    def save_graph(self, project_id: str, graph: Graph):
        pass
