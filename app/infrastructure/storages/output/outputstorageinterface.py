from abc import ABC, abstractmethod
from typing import List

from app.core.valueobjects import File


class IOutputStorage(ABC):
    @abstractmethod
    def create_folder_structure(self, folder_name: str):
        pass

    @abstractmethod
    def save_file(self, folder_name: str, schema_file: File):
        pass

    @abstractmethod
    def save_files(self, folder_name: str, static_files: List[File]):
        pass
