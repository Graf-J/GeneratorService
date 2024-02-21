from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.entities import Edge, Property


class Vertex:
    def __init__(
            self,
            _id: str,
            name: str,
            position_x: int,
            position_y: int,
            radius: int,
            properties: List['Property']
    ):
        self.id = _id
        self.name = name
        self.position_x = position_x
        self.position_y = position_y
        self.radius = radius
        self.properties = properties

        self.out_edges: List[Edge] = []
        self.in_edges: List[Edge] = []

    def add_out_edge(self, edge: 'Edge'):
        self.out_edges.append(edge)

    def add_in_edge(self, edge: 'Edge'):
        self.in_edges.append(edge)
