import os
import pickle
from typing import List

from app.core.entities import Project, Graph


class ProjectFolderAdapter:
    def __init__(self, project_folder='projects'):
        self.project_folder = project_folder

    def get_project_files(self) -> List[str]:
        base_directory = os.getcwd()
        path = os.path.join(base_directory, self.project_folder)
        project_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f != '.gitkeep']

        return project_files

    def generate_project_path(self, project: Project):
        base_directory = os.getcwd()
        path = os.path.join(base_directory, self.project_folder, f'{project.name}_{project.id}.pickle')

        return path

    def read_pickle(self, path: str) -> Graph:
        with open(path, 'rb') as file:
            graph = pickle.load(file)

        return graph

    def write_pickle(self, path: str, graph: Graph):
        with open(path, 'wb') as file:
            pickle.dump(graph, file, protocol=pickle.HIGHEST_PROTOCOL)
