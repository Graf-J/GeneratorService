from typing import List

from app.core.entities import Project
from app.core.valueobjects import File
from app.infrastructure.adapters import OutputFolderAdapter
from app.infrastructure.storages.output.outputstorageinterface import IOutputStorage


class OutputStorage(IOutputStorage):
    output_folder = 'outputs'
    graph_folder = 'graph'
    querybuilder_folder = 'querybuilder'
    arguments_folder = 'arguments'

    def __init__(self, folder_adapter: OutputFolderAdapter):
        self.folder_adapter = folder_adapter

    def create_folder_structure(self, folder_name: str):
        self.folder_adapter.delete_output_folder_if_exists(folder_name)
        self.folder_adapter.create_output_folder(folder_name)
        self.folder_adapter.create_graph_folder(folder_name)
        self.folder_adapter.create_querybuilder_folder(folder_name)

    def save_schema_file(self, project: Project, schema_file: File):
        self.folder_adapter.save_file([project.name], schema_file)

    def save_app_file(self, project: Project, app_file: File):
        self.folder_adapter.save_file([project.name], app_file)

    def save_docker_compose_file(self, project: Project, docker_compose_file: File):
        self.folder_adapter.save_file([project.name], docker_compose_file)

    def save_graph_json_file(self, project: Project, graph_json_file: File):
        self.folder_adapter.save_file([project.name], graph_json_file)

    def save_graph_files(self, project: Project, graph_files: List[File]):
        for file in graph_files:
            self.folder_adapter.save_file([project.name, self.graph_folder], file)

    def save_querybuilder_files(self, project: Project, querybuilder_files: List[File]):
        for file in querybuilder_files:
            self.folder_adapter.save_file([project.name, self.querybuilder_folder], file)

    def save_querybuilder_argument_files(self, project: Project, querybuilder_argument_files: List[File]):
        for file in querybuilder_argument_files:
            self.folder_adapter.save_file([project.name, self.querybuilder_folder, self.arguments_folder], file)

    def save_static_files(self, project: Project, static_files: List[File]):
        for file in static_files:
            self.folder_adapter.save_file([project.name], file)
