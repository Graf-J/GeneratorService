from typing import List

from app.core.repositories.output.outputrepositoryinterface import IOutputRepository
from app.core.valueobjects import File
from app.infrastructure.storages.output.outputstorageinterface import IOutputStorage


class OutputRepository(IOutputRepository):
    def __init__(self, storage: IOutputStorage):
        self.storage = storage

    def create_folder_structure(self, project_name: str):
        self.storage.create_folder_structure(project_name)

    def save_file(self, path: List[str], file: File):
        self.storage.save_file(path, file)

    def save_files(self, path: List[str], files: List[File]):
        self.storage.save_files(path, files)
