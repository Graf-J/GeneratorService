from typing import List

from app.core.entities import Project
from app.core.repositories.project.projectrepositoryinterface import IProjectRepository
from app.infrastructure.storage import IStorage


class ProjectRepository(IProjectRepository):
    def __init__(self, storage: IStorage):
        self.storage = storage

    def get_projects(self) -> List[Project]:
        projects = self.storage.get_projects()

        return projects

    def get_project(self, project_id: str) -> Project:
        project = self.storage.get_project(project_id)

        return project

    def create_project(self, project: Project) -> Project:
        project = self.storage.create_project(project)

        return project

    def delete_project(self, project_id: str):
        self.storage.delete_project(project_id)
