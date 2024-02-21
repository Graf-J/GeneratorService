from app.core.exceptions import ProjectException


class ProjectNotFoundException(ProjectException):
    def __init__(self, message):
        self.message = message
        super().__init__(message)
