from app.core.entities import Project
from app.core.repositories import IProjectRepository, IOutputRepository
from app.core.services.project.projectserviceinterface import IProjectService


class ProjectService(IProjectService):
    def __init__(self, project_repository: IProjectRepository, output_repository: IOutputRepository):
        self.project_repository = project_repository
        self.output_repository = output_repository

    def get_projects(self):
        projects = self.project_repository.get_projects()

        return projects

    def get_project(self, project_id: str) -> Project:
        project = self.project_repository.get_project(project_id)

        return project

    def create_project(self, project: Project):
        project = self.project_repository.create_project(project)

        return project

    def delete_project(self, project_id: str, delete_output: bool):
        project = self.project_repository.get_project(project_id)
        self.project_repository.delete_project(project_id)

        if delete_output:
            self.output_repository.delete_output_folder_if_exists(project)
