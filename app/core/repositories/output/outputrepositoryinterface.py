from abc import ABC, abstractmethod
from typing import List

from app.core.entities import Project
from app.core.valueobjects import File


class IOutputRepository(ABC):
    @abstractmethod
    def create_folder_structure(self, project_name: str):
        pass

    @abstractmethod
    def save_schema_file(self, project: Project, schema_file: File):
        pass

    @abstractmethod
    def save_app_file(self, project: Project, app_file: File):
        pass

    @abstractmethod
    def save_docker_compose_file(self, project: Project, docker_compose_file: File):
        pass

    @abstractmethod
    def save_graph_json_file(self, project: Project, graph_json_file: File):
        pass

    @abstractmethod
    def save_graph_files(self, project: Project, graph_files: List[File]):
        pass

    @abstractmethod
    def save_querybuilder_files(self, project: Project, querybuilder_files: List[File]):
        pass

    @abstractmethod
    def save_querybuilder_argument_files(self, project: Project, querybuilder_argument_files: List[File]):
        pass

    @abstractmethod
    def save_static_files(self, project: Project, static_files: List[File]):
        pass
