import uuid

from app.api.dto import ProjectRequestDto, ProjectResponseDto
from app.core.entities import Project
from app.mappers import Mapper


class ProjectMapper(Mapper):
    @staticmethod
    def to_entity(dto: ProjectRequestDto) -> Project:
        project_entity = Project(
            _id=str(uuid.uuid4()),
            name=dto.name
        )

        return project_entity

    @staticmethod
    def to_dto(entity: Project) -> ProjectResponseDto:
        project_dto = ProjectResponseDto(
            id=entity.id,
            name=entity.name
        )

        return project_dto
