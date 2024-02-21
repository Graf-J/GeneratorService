from app.core.exceptions import EdgeException


class EdgeNotFoundException(EdgeException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
