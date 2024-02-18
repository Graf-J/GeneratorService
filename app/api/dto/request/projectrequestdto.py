import re

from pydantic import BaseModel, Field, field_validator


class ProjectRequestDto(BaseModel):
    name: str = Field(..., min_length=1)

    @field_validator('name')
    def validate_name(cls, value: str) -> str:
        # Check for forbidden characters
        forbidden_characters = r'[\\/:"*?<>,|]'
        if re.search(forbidden_characters, value):
            raise ValueError("Invalid characters in the filename.")

        # Check for unwanted characters
        unwanted_characters = r'[_\säÄöÖüÜß.]'
        if re.search(unwanted_characters, value):
            raise ValueError("Filenames should not contain underscores, spaces, dots, or special characters.")

        return value
