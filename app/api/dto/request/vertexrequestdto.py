import re
from typing import List

from pydantic import BaseModel, Field, field_validator

from app.api.dto import PropertyDto


class VertexRequestDto(BaseModel):
    name: str = Field(..., min_length=1)
    position_x: int
    position_y: int
    properties: List[PropertyDto]

    @field_validator('name')
    def validate_name(cls, value: str) -> str:
        # Check for invalid special characters
        if not re.match(r'^[_a-zA-Z][_a-zA-Z0-9]*$', value):
            raise ValueError(
                "Name must start with a letter or underscore, followed by letters, numbers, or underscores.")

        # Check if name starts with two underscores
        if value.startswith('__'):
            raise ValueError("Name that starts with '__' is not allowed")

        return value

    @field_validator('properties')
    def check_duplicate_keys(cls, properties: List[PropertyDto]) -> List[PropertyDto]:
        keys_seen = set()
        for prop in properties:
            # Check for Duplicate
            if prop.key in keys_seen:
                raise ValueError(f"Duplicate key detected in properties: {prop.key}")

            keys_seen.add(prop.key)

        return properties
