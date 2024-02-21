from app.core.exceptions import VertexException


class VertexNotFoundException(VertexException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
