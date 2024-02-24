from abc import ABC, abstractmethod

from jinja2 import Template


class IOutputRepository(ABC):
    @abstractmethod
    def get_schema_template(self, project_name: str) -> Template:
        pass

    @abstractmethod
    def create_folder_structure(self, project_name: str):
        pass

    @abstractmethod
    def insert_schema(self, project_name: str, schema_content: str):
        pass

    @abstractmethod
    def insert_main_py(self, project_name: str, main_py_content: str):
        pass

    @abstractmethod
    def insert_dockerfile(self, project_name: str, dockerfile_content: str):
        pass

    @abstractmethod
    def copy_static_files(self, project_name: str):
        pass
