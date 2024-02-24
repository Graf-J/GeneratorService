from jinja2 import Template

from app.core.repositories.output.outputrepositoryinterface import IOutputRepository
from app.infrastructure.storages.output.outputstorageinterface import IOutputStorage


class OutputRepository(IOutputRepository):

    def __init__(self, storage: IOutputStorage):
        self.storage = storage

    def get_schema_template(self, project_name: str) -> Template:
        schema_template = self.storage.get_schema_template(project_name)

        return schema_template

    def create_folder_structure(self, project_name: str):
        self.storage.create_folder_structure(project_name)

    def insert_schema(self, project_name: str, schema_content: str):
        self.storage.insert_schema_content(project_name, schema_content)

    def insert_main_py(self, project_name: str, main_py_content: str):
        pass

    def insert_dockerfile(self, project_name: str, dockerfile_content: str):
        pass

    def copy_static_files(self, project_name: str):
        self.storage.copy_static_files(project_name)
