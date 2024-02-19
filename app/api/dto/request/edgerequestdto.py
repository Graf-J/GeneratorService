from typing import List

from pydantic import BaseModel, Field, UUID4

from app.api.dto import PropertyDto


class EdgeRequestDto(BaseModel):
    name: str = Field(..., min_length=1)
    properties: List[PropertyDto]
    source_vertex_id: UUID4
    target_vertex_id: UUID4
