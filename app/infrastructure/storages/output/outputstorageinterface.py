from abc import ABC, abstractmethod

from jinja2 import Template


class IOutputStorage(ABC):
    @abstractmethod
    def get_schema_template(self, folder_name: str) -> Template:
        pass

    @abstractmethod
    def create_folder_structure(self, folder_name: str):
        pass

    @abstractmethod
    def insert_schema_content(self, folder_name: str, schema_content: str):
        pass

    @abstractmethod
    def copy_static_files(self, folder_name: str):
        pass
