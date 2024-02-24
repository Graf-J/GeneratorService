from abc import ABC, abstractmethod


class IBuildService(ABC):
    @abstractmethod
    def build_project(self, project_id: str):
        pass
