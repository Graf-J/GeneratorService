class Datatype:
    STRING = 'String'
    INT = 'Int'
    FLOAT = 'Float'
    BOOLEAN = 'Boolean'


class Property:
    def __init__(self, key: str, required: bool, datatype: Datatype):
        self.key = key
        self.required = required
        self.datatype = datatype

    def to_dict(self) -> dict:
        return {
            'field_name': self.key
        }
