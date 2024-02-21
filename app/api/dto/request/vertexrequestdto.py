import re
from typing import List

from pydantic import BaseModel, Field, field_validator

from app.api.dto import PropertyDto


class VertexRequestDto(BaseModel):
    name: str = Field(..., min_length=1)
    position_x: int
    position_y: int
    radius: int
    properties: List[PropertyDto]

    @field_validator('name')
    def validate_name(cls, value: str) -> str:
        if not re.match(r'^[_a-zA-Z][_a-zA-Z0-9]*$', value):
            raise ValueError(
                "Name must start with a letter or underscore, followed by letters, numbers, or underscores.")

        return value
