from abc import ABC, abstractmethod

from app.core.entities import Build


class IBuildService(ABC):
    @abstractmethod
    def build_project(self, project_id: str, build_config: Build):
        pass
