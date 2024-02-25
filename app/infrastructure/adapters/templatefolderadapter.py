import os
from typing import List

from jinja2 import Template, Environment, FileSystemLoader

from app.core.valueobjects import File


class TemplateFolderAdapter:
    def __init__(
            self,
            template_folder='templates',
            schema_folder='schema',
            app_folder='app',
            static_folder='static',
            graph_folder='graph'
    ):
        self.template_folder = template_folder
        self.schema_folder = schema_folder
        self.app_folder = app_folder
        self.static_folder = static_folder
        self.graph_folder = graph_folder

    def get_schema_template(self, schema_template_file_name='schema.jinja') -> Template:
        base_directory = os.getcwd()
        path = os.path.join(base_directory, self.template_folder, self.schema_folder)

        env = Environment(loader=FileSystemLoader(path))
        template = env.get_template(schema_template_file_name)

        return template

    def get_app_template(self, app_template_file_name='app.jinja'):
        base_directory = os.getcwd()
        path = os.path.join(base_directory, self.template_folder, self.app_folder)

        env = Environment(loader=FileSystemLoader(path))
        template = env.get_template(app_template_file_name)

        return template

    def get_graph_files(self):
        base_directory = os.getcwd()
        files = self.get_files(base_directory, self.graph_folder)

        return files

    def get_static_files(self) -> List[File]:
        base_directory = os.getcwd()
        files = self.get_files(base_directory, self.static_folder)

        return files

    def get_files(self, base_directory: str, files_folder: str):
        files: List[File] = []

        for file_name in os.listdir(os.path.join(base_directory, self.template_folder, files_folder)):
            file_path = os.path.join(base_directory, self.template_folder, files_folder, file_name)
            with open(file_path, 'rb') as file:
                files.append(File(file_name=file_name, byte_content=file.read()))

        return files
