import os
from typing import List

from jinja2 import Template, Environment, FileSystemLoader

from app.core.valueobjects import File


class TemplateFolderAdapter:
    def get_template(self, path: List[str], template_file_name: str) -> Template:
        base_directory = os.getcwd()
        full_path = os.path.join(base_directory, *path)

        env = Environment(loader=FileSystemLoader(full_path))
        template = env.get_template(template_file_name)

        return template

    def get_files(self, path: List[str]) -> List[File]:
        base_directory = os.getcwd()

        files: List[File] = []
        full_path = os.path.join(base_directory, *path)
        # for file_name in os.listdir(os.path.join(base_directory, self.template_folder, *path)):
        for file_name in [f for f in os.listdir(full_path) if os.path.isfile(os.path.join(full_path, f))]:
            file_path = os.path.join(base_directory, *path, file_name)
            with open(file_path, 'rb') as file:
                files.append(File(file_name=file_name, byte_content=file.read()))

        return files
