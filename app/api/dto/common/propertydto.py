from enum import Enum
from pydantic import BaseModel


class Datatype(str, Enum):
    STRING = 'String'
    INT = 'Int'
    FLOAT = 'Float'
    BOOLEAN = 'Boolean'
    ID = 'ID'


class PropertyDto(BaseModel):
    key: str
    required: bool
    datatype: Datatype
