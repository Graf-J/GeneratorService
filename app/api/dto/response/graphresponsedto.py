from typing import List

from pydantic import BaseModel

from app.api.dto.response.edgeresponsedto import EdgeResponseDto
from app.api.dto.response.vertexresponsedto import VertexResponseDto


class GraphResponseDto(BaseModel):
    vertices: List[VertexResponseDto]
    edges: List[EdgeResponseDto]
