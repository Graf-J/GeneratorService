from typing import Optional

from pydantic import BaseModel, field_validator, constr


class BuildRequestDto(BaseModel):
    port: int
    volume: Optional[constr(min_length=1)] = None

    @field_validator('port')
    def validate_port(cls, value: int) -> int:
        if not (0 <= value <= 65535):
            raise ValueError('Port must be in the range 0 to 65535')

        return value

    @field_validator('volume')
    def validate_volume(cls, value: str):
        if not all(char.isalnum() or char in {'_', '-'} for char in value):
            raise ValueError('Volume name must contain only alphanumeric characters, underscores, or hyphens')

        return value
