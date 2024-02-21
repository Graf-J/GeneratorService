from typing import List

from app.core.entities import Project
from app.core.exceptions import ProjectNotFoundException, ProjectException
from app.core.repositories.project.projectrepositoryinterface import IProjectRepository
from app.infrastructure.storage import IStorage


class ProjectRepository(IProjectRepository):
    def __init__(self, storage: IStorage):
        self.storage = storage

    def get_projects(self) -> List[Project]:
        projects = self.storage.get_projects()

        return projects

    def get_project(self, project_id: str) -> Project:
        try:
            project = self.storage.get_project(project_id)

            return project
        except ValueError as ex:
            raise ProjectNotFoundException(str(ex))

    def create_project(self, project: Project) -> Project:
        # Check if Project with name already exists
        existing_projects = self.storage.get_projects()
        existing_project_names = [existing_project.name for existing_project in existing_projects]
        if project.name in existing_project_names:
            raise ProjectException(f"Project '{project.name}' already exists")

        # Create Project
        project = self.storage.create_project(project)

        return project

    def delete_project(self, project_id: str):
        try:
            self.storage.delete_project(project_id)
        except ValueError as ex:
            raise ProjectNotFoundException(str(ex))
