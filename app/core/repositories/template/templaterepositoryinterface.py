from abc import ABC, abstractmethod
from typing import List

from jinja2 import Template

from app.core.valueobjects import File


class ITemplateRepository(ABC):
    @abstractmethod
    def get_schema_template(self) -> Template:
        pass

    @abstractmethod
    def get_app_template(self) -> Template:
        pass

    @abstractmethod
    def get_graph_files(self) -> List[File]:
        pass

    @abstractmethod
    def get_static_files(self) -> List[File]:
        pass
