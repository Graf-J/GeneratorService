import os
from typing import List

from app.core.entities import Graph, Project
from app.infrastructure.storage import IStorage
from app.infrastructure.utils import FileManager


class PickleStorage(IStorage):
    def __init__(self, filemanager: FileManager):
        self.filemanager = filemanager

    def get_projects(self) -> List[Project]:
        project_files = self.filemanager.get_project_files()

        projects = []
        for file in project_files:
            file_name = file.split('.')[0]
            name, _id = file_name.split('_')
            projects.append(Project(_id, name))

        return projects

    def get_project(self, project_id: str) -> Project:
        projects = self.get_projects()
        for project in projects:
            if project.id == project_id:
                return project

        raise ValueError('Project not found')

    def create_project(self, project: Project) -> Project:
        path = self.filemanager.generate_project_path(project)

        graph = Graph()
        self.filemanager.write_pickle(path, graph)

        return project

    def delete_project(self, project_id: str):
        project = self.get_project(project_id)
        path = self.filemanager.generate_project_path(project)

        os.remove(path)

    def load_graph(self, project_id: str) -> Graph:
        project = self.get_project(project_id)
        path = self.filemanager.generate_project_path(project)
        graph = self.filemanager.read_pickle(path)

        return graph

    def save_graph(self, project_id: str, graph: Graph):
        project = self.get_project(project_id)
        path = self.filemanager.generate_project_path(project)
        self.filemanager.write_pickle(path, graph)
