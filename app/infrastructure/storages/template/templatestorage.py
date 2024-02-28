from typing import List

from jinja2 import Template

from app.core.valueobjects import File
from app.infrastructure.adapters.templatefolderadapter import TemplateFolderAdapter
from app.infrastructure.storages.template.templatestorageinterface import ITemplateStorage


class TemplateStorage(ITemplateStorage):
    template_folder = 'templates'
    schema_folder = 'schema'
    app_folder = 'app'
    docker_compose_folder = 'docker_compose'
    graph_folder = 'graph'
    querybuilder_folder = 'querybuilder'
    arguments_folder = 'arguments'
    static_folder = 'static'
    schema_template_file_name = 'schema.jinja'
    app_template_file_name = 'app.jinja'
    docker_compose_template_file_name = 'docker-compose.jinja'

    def __init__(self, folder_adapter: TemplateFolderAdapter):
        self.folder_adapter = folder_adapter

    def get_schema_template(self) -> Template:
        schema_template = self.folder_adapter.get_template([self.template_folder, self.schema_folder],
                                                           self.schema_template_file_name)

        return schema_template

    def get_app_template(self) -> Template:
        app_template = self.folder_adapter.get_template([self.template_folder, self.app_folder],
                                                        self.app_template_file_name)

        return app_template

    def get_docker_compose_template(self) -> Template:
        docker_compose_template = self.folder_adapter.get_template([self.template_folder, self.docker_compose_folder],
                                                                   self.docker_compose_template_file_name)

        return docker_compose_template

    def get_graph_files(self) -> List[File]:
        files = self.folder_adapter.get_files([self.template_folder, self.graph_folder])

        return files

    def get_querybuilder_files(self) -> List[File]:
        files = self.folder_adapter.get_files([self.template_folder, self.querybuilder_folder])

        return files

    def get_querybuilder_argument_files(self) -> List[File]:
        files = self.folder_adapter.get_files([self.template_folder, self.querybuilder_folder, self.arguments_folder])

        return files

    def get_static_files(self) -> List[File]:
        files = self.folder_adapter.get_files([self.template_folder, self.static_folder])

        return files
