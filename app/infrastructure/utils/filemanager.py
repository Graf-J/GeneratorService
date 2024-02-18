import os
from typing import List

from app.core.entities import Project


class FileManager:
    def __init__(self, project_folder='projects'):
        self.project_folder = project_folder

    def get_project_files(self) -> List[str]:
        base_directory = os.getcwd()
        path = os.path.join(base_directory, self.project_folder)
        project_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

        return project_files

    def generate_project_path(self, project: Project):
        base_directory = os.getcwd()
        path = os.path.join(base_directory, self.project_folder, f'{project.name}_{project.id}.pickle')

        return path
