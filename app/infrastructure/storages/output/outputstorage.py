from typing import List

from app.core.valueobjects import File
from app.infrastructure.adapters import OutputFolderAdapter
from app.infrastructure.storages.output.outputstorageinterface import IOutputStorage


class OutputStorage(IOutputStorage):
    def __init__(self, folder_adapter: OutputFolderAdapter):
        self.folder_adapter = folder_adapter

    def create_folder_structure(self, folder_name: str):
        self.folder_adapter.delete_output_folder_if_exists(folder_name)
        self.folder_adapter.create_output_folder(folder_name)

    def save_file(self, folder_name: str, file: File):
        self.folder_adapter.save_file(folder_name, file)

    def save_files(self, folder_name: str, files: List[File]):
        for file in files:
            self.folder_adapter.save_file(folder_name, file)
