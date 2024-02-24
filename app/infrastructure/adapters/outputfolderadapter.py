import os
import shutil

from app.core.valueobjects import File


class OutputFolderAdapter:
    def __init__(self, output_folder='outputs'):
        self.output_folder = output_folder

    def delete_output_folder_if_exists(self, folder_name: str):
        base_directory = os.getcwd()
        path = os.path.join(base_directory, self.output_folder, folder_name)

        if os.path.exists(path):
            shutil.rmtree(path)

    def create_output_folder(self, folder_name: str):
        base_directory = os.getcwd()
        path = os.path.join(base_directory, self.output_folder, folder_name)

        os.makedirs(path, exist_ok=True)

    def save_file(self, folder_name: str, file: File):
        base_directory = os.getcwd()
        path = os.path.join(base_directory, self.output_folder, folder_name, file.file_name)

        with open(path, 'wb') as out_file:
            out_file.write(file.byte_content)
