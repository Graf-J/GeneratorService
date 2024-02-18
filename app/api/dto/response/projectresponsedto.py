from pydantic import UUID4
from app.api.dto import ProjectRequestDto


class ProjectResponseDto(ProjectRequestDto):
    id: UUID4
