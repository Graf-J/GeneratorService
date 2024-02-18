from typing import List
from app.core.entities.property import Property


class Vertex:
    def __init__(
            self,
            _id: str,
            name: str,
            position_x: int,
            position_y: int,
            radius: int,
            properties: List[Property]
    ):
        self.id = _id
        self.name = name
        self.position_x = position_x
        self.position_y = position_y
        self.radius = radius
        self.properties = properties

        self.out_edges = []
        self.in_edges = []

    def add_out_edge(self):
        pass

    def add_in_edge(self):
        pass
