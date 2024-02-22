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
                raise ValueError(f"Duplicate key found in properties: {prop.key}")

            # Check for forbidden keys ("id" or "label")
            if prop.key == 'id':
                raise ValueError("Property with key 'id' is not allowed")
            if prop.key == 'label':
                raise ValueError("Property with key 'label' is not allowed")

            # Check if key starts with two underscores
            if prop.key.startswith('__'):
                raise ValueError("Property with key that starts with '__' is not allowed")

            keys_seen.add(prop.key)

        return properties
