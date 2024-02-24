from abc import ABC, abstractmethod
from typing import List

from jinja2 import Template

from app.core.valueobjects import File


class ITemplateStorage(ABC):
    @abstractmethod
    def get_schema_template(self) -> Template:
        pass

    @abstractmethod
    def get_static_files(self) -> List[File]:
        pass
