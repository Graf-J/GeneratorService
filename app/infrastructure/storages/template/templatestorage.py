from typing import List

from jinja2 import Template

from app.core.valueobjects import File
from app.infrastructure.adapters.templatefolderadapter import TemplateFolderAdapter
from app.infrastructure.storages.template.templatestorageinterface import ITemplateStorage


class TemplateStorage(ITemplateStorage):
    def __init__(self, folder_adapter: TemplateFolderAdapter):
        self.folder_adapter = folder_adapter

    def get_schema_template(self) -> Template:
        schema_template = self.folder_adapter.get_schema_template()

        return schema_template

    def get_app_template(self) -> Template:
        app_template = self.folder_adapter.get_app_template()

        return app_template

    def get_files(self, path: List[str]) -> List[File]:
        files = self.folder_adapter.get_files(path)

        return files
