from abc import ABC, abstractmethod
from typing import List

from app.core.valueobjects import File


class IOutputStorage(ABC):
    @abstractmethod
    def create_folder_structure(self, folder_name: str):
        pass

    @abstractmethod
    def save_file(self, path: List[str], schema_file: File):
        pass

    @abstractmethod
    def save_files(self, path: List[str], files: List[File]):
        pass
