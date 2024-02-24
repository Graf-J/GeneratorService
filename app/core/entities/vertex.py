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

    @property
    def name_upper(self) -> str:
        return self.name[0].upper() + self.name[1:]

    @property
    def name_lower(self) -> str:
        return self.name[0].lower() + self.name[1:]

    @property
    def type_name(self) -> str:
        return self.name_upper + 'Vertex'

    @property
    def logic_input_name(self) -> str:
        return self.name_upper + 'VertexLogicInput'

    @property
    def order_by_input_name(self) -> str:
        return self.name_upper + 'VertexOrderByInput'

    @property
    def add_input_name(self) -> str:
        return 'Add' + self.name_upper + 'VertexInput'

    @property
    def update_input_name(self) -> str:
        return 'Update' + self.name_upper + 'VertexInput'

    @property
    def property_name(self) -> str:
        return self.name_upper + 'VertexProperty'

    def has_properties(self) -> bool:
        return len(self.properties) > 0

    def add_out_edge(self, edge: 'Edge'):
        self.out_edges.append(edge)

    def add_in_edge(self, edge: 'Edge'):
        self.in_edges.append(edge)
