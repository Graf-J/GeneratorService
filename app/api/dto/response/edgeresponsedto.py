from pydantic import UUID4

from app.api.dto import EdgeRequestDto


class EdgeResponseDto(EdgeRequestDto):
    id: UUID4
