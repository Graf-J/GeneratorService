class Datatype:
    STRING = 'String'
    INT = 'Int'
    FLOAT = 'Float'


class Property:
    def __init__(self, key: str, required: bool, datatype: Datatype):
        self.key = key
        self.required = required
        self.datatype = datatype
