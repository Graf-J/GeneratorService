from pydantic import UUID4
from app.api.dto import VertexRequestDto


class VertexResponseDto(VertexRequestDto):
    id: UUID4
