from jinja2 import Template

from app.infrastructure.adapters import OutputFolderAdapter
from app.infrastructure.storages.output.outputstorageinterface import IOutputStorage


class OutputStorage(IOutputStorage):

    def __init__(self, folder_adapter: OutputFolderAdapter):
        self.folder_adapter = folder_adapter

    def get_schema_template(self, folder_name: str) -> Template:
        schema_template = self.folder_adapter.get_schema_template()

        return schema_template

    def create_folder_structure(self, folder_name: str):
        self.folder_adapter.delete_output_folder_if_exists(folder_name)
        self.folder_adapter.create_output_folder(folder_name)

    def insert_schema_content(self, folder_name: str, schema_content: str):
        self.folder_adapter.save_content_to_file(folder_name, 'schema.py', schema_content)

    def copy_static_files(self, folder_name: str):
        static_file_names = self.folder_adapter.get_static_files()
        self.folder_adapter.copy_static_files(folder_name, static_file_names)
