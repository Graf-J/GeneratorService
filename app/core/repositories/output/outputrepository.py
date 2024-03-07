from typing import List

from app.core.entities import Project
from app.core.repositories.output.outputrepositoryinterface import IOutputRepository
from app.core.valueobjects import File
from app.infrastructure.storages.output.outputstorageinterface import IOutputStorage


class OutputRepository(IOutputRepository):
    def __init__(self, storage: IOutputStorage):
        self.storage = storage

    def delete_output_folder_if_exists(self, project: Project):
        self.storage.delete_output_folder_if_exists(project)

    def create_folder_structure(self, project: Project):
        self.storage.create_folder_structure(project)

    def save_schema_file(self, project: Project, schema_file: File):
        self.storage.save_schema_file(project, schema_file)

    def save_app_file(self, project: Project, app_file: File):
        self.storage.save_app_file(project, app_file)

    def save_docker_compose_file(self, project: Project, docker_compose_file: File):
        self.storage.save_docker_compose_file(project, docker_compose_file)

    def save_graph_json_file(self, project: Project, graph_json_file: File):
        self.storage.save_graph_json_file(project, graph_json_file)

    def save_graph_files(self, project: Project, graph_files: List[File]):
        self.storage.save_graph_files(project, graph_files)

    def save_querybuilder_files(self, project: Project, querybuilder_files: List[File]):
        self.storage.save_querybuilder_files(project, querybuilder_files)

    def save_querybuilder_argument_files(self, project: Project, querybuilder_argument_files: List[File]):
        self.storage.save_querybuilder_argument_files(project, querybuilder_argument_files)

    def save_static_files(self, project: Project, static_files: List[File]):
        self.storage.save_static_files(project, static_files)
