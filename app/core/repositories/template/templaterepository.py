from typing import List

from jinja2 import Template

from app.core.repositories.template.templaterepositoryinterface import ITemplateRepository
from app.core.valueobjects import File
from app.infrastructure.storages import ITemplateStorage


class TemplateRepository(ITemplateRepository):
    def __init__(self, storage: ITemplateStorage):
        self.storage = storage

    def get_schema_template(self) -> Template:
        schema_template = self.storage.get_schema_template()

        return schema_template

    def get_app_template(self) -> Template:
        app_template = self.storage.get_app_template()

        return app_template

    def get_graph_files(self) -> List[File]:
        graph_files = self.storage.get_graph_files()

        return graph_files

    def get_static_files(self) -> List[File]:
        static_files = self.storage.get_static_files()

        return static_files
