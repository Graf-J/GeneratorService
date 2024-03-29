import os
import shutil
from typing import List

from app.core.exceptions import DeleteOutputException
from app.core.valueobjects import File


class OutputFolderAdapter:
    def __init__(
            self,
            output_folder='outputs',
            graph_folder='graph',
            querybuilder_folder='querybuilder',
            querybuilder_arguments_folder='arguments'
    ):
        self.output_folder = output_folder
        self.graph_folder = graph_folder
        self.querybuilder_folder = querybuilder_folder
        self.querybuilder_arguments_folder = querybuilder_arguments_folder

    def delete_output_folder_if_exists(self, folder_name: str):
        try:
            base_directory = os.getcwd()
            path = os.path.join(base_directory, self.output_folder, folder_name)

            if os.path.exists(path):
                shutil.rmtree(path)
        except PermissionError:
            raise DeleteOutputException("Another Process is accessing the output folder")

    def create_output_folder(self, folder_name: str):
        base_directory = os.getcwd()
        path = os.path.join(base_directory, self.output_folder, folder_name)

        os.makedirs(path, exist_ok=True)

    def create_graph_folder(self, root_folder: str):
        base_directory = os.getcwd()
        path = os.path.join(base_directory, self.output_folder, root_folder, self.graph_folder)

        os.makedirs(path, exist_ok=True)

    def create_querybuilder_folder(self, root_folder: str):
        base_directory = os.getcwd()

        # Create querybuilder Folder
        querybuilder_path = os.path.join(base_directory, self.output_folder, root_folder, self.querybuilder_folder)
        os.makedirs(querybuilder_path, exist_ok=True)
        # Create arguments Folder inside querybuilder Folder
        arguments_path = os.path.join(base_directory, self.output_folder, root_folder, self.querybuilder_folder,
                                      self.querybuilder_arguments_folder)
        os.makedirs(arguments_path, exist_ok=True)

    def save_file(self, path: List[str], file: File):
        base_directory = os.getcwd()
        path = os.path.join(base_directory, self.output_folder, *path, file.file_name)

        with open(path, 'wb') as out_file:
            out_file.write(file.byte_content)
