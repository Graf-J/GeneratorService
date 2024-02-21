from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.entities import Property, Vertex


class Edge:
    def __init__(
            self,
            _id: str,
            name: str,
            properties: List['Property'],
    ):
        self.id = _id
        self.name = name
        self.properties = properties
        self.source_vertex: Vertex | None = None
        self.target_vertex: Vertex | None = None
