from app.core.entities import Project
from app.core.repositories import IProjectRepository
from app.core.services.project.projectserviceinterface import IProjectService


class ProjectService(IProjectService):
    def __init__(self, repository: IProjectRepository):
        self.repository = repository

    def get_projects(self):
        projects = self.repository.get_projects()

        return projects

    def get_project(self, project_id: str) -> Project:
        project = self.repository.get_project(project_id)

        return project

    def create_project(self, project: Project):
        project = self.repository.create_project(project)

        return project

    def delete_project(self, project_id: str):
        self.repository.delete_project(project_id)
