from typing import List

from pydantic import UUID4

from app.api.dto import VertexRequestDto, EdgeResponseDto


class VertexResponseDto(VertexRequestDto):
    id: UUID4
    out_edges: List[EdgeResponseDto]
    in_edges: List[EdgeResponseDto]
