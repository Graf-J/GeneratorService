import re
from enum import Enum

from pydantic import BaseModel, field_validator


class Datatype(str, Enum):
    STRING = 'String'
    INT = 'Int'
    FLOAT = 'Float'
    BOOLEAN = 'Boolean'


class PropertyDto(BaseModel):
    key: str
    required: bool
    datatype: Datatype

    @field_validator('key')
    def validate_name(cls, key: str) -> str:
        # Check for overall structure
        if not re.match(r'^[_a-zA-Z][_a-zA-Z0-9]*$', key):
            raise ValueError(
                "Key must start with a letter or underscore, followed by letters, numbers, or underscores.")

        # Check for forbidden keys ("id" or "label")
        if key == 'id':
            raise ValueError("Property with key 'id' is not allowed")
        if key == 'label':
            raise ValueError("Property with key 'label' is not allowed")

        # Check if key starts with two underscores
        if key.startswith('__'):
            raise ValueError("Property with key that starts with '__' is not allowed")

        return key
