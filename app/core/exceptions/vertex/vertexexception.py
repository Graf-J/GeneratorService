class VertexException(Exception):
    def __init__(self, message: str, status_code: int, loc: str):
        self.message = message
        self.status_code = status_code
        self.loc = loc
        super().__init__(self.message)
