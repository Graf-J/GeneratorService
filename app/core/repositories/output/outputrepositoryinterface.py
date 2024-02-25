from abc import ABC, abstractmethod
from typing import List

from app.core.valueobjects import File


class IOutputRepository(ABC):
    @abstractmethod
    def create_folder_structure(self, project_name: str):
        pass

    @abstractmethod
    def save_file(self, path: List[str], file: File):
        pass

    @abstractmethod
    def save_files(self, path: List[str], files: List[File]):
        pass
