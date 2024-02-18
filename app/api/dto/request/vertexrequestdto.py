from pydantic import BaseModel, Field
from typing import List
from app.api.dto import PropertyDto


class VertexRequestDto(BaseModel):
    name: str = Field(..., min_length=1)
    position_x: int
    position_y: int
    radius: int
    properties: List[PropertyDto]
