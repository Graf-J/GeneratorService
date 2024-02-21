import re
from typing import List

from pydantic import BaseModel, Field, UUID4, field_validator

from app.api.dto import PropertyDto


class EdgeRequestDto(BaseModel):
    name: str = Field(..., min_length=1)
    properties: List[PropertyDto]
    source_vertex_id: UUID4
    target_vertex_id: UUID4

    @field_validator('name')
    def validate_name(cls, value: str) -> str:
        if not re.match(r'^[_a-zA-Z][_a-zA-Z0-9]*$', value):
            raise ValueError(
                "Name must start with a letter or underscore, followed by letters, numbers, or underscores.")

        return value
