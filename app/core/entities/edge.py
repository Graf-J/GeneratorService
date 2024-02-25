from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.entities import Property, Vertex


class Edge:
    def __init__(
            self,
            _id: str,
            name: str,
            properties: List['Property'],
            multi_edge: bool
    ):
        self.id = _id
        self.name = name
        self.properties = properties
        self.multi_edge = multi_edge
        self.source_vertex: Vertex | None = None
        self.target_vertex: Vertex | None = None

    @property
    def name_upper(self) -> str:
        return self.name[0].upper() + self.name[1:]

    @property
    def name_lower(self) -> str:
        return self.name[0].lower() + self.name[1:]

    @property
    def out_type_name(self) -> str:
        return self.source_vertex.name_upper + 'To' + self.target_vertex.name_upper + self.name_upper + 'Edge'

    @property
    def in_type_name(self) -> str:
        return self.target_vertex.name_upper + 'To' + self.source_vertex.name_upper + self.name_upper + 'Edge'

    @property
    def out_field_name(self) -> str:
        return self.name_lower + 'Out'

    @property
    def in_field_name(self) -> str:
        return self.name_lower + 'In'

    @property
    def logic_input_name(self) -> str:
        return self.source_vertex.name_upper + 'To' + self.target_vertex.name_upper + self.name_upper + 'EdgeLogicInput'

    @property
    def order_by_input_name(self) -> str:
        return self.source_vertex.name_upper + 'To' + self.target_vertex.name_upper + self.name_upper + 'EdgeOrderByInput'

    @property
    def add_input_name(self) -> str:
        return 'Add' + self.source_vertex.name_upper + 'To' + self.target_vertex.name_upper + 'Via' + self.name_upper + 'EdgeInput'

    @property
    def update_input_name(self):
        return 'Update' + self.source_vertex.name_upper + 'To' + self.target_vertex.name_upper + 'Via' + self.name_upper + 'EdgeInput'

    @property
    def property_name(self) -> str:
        return self.source_vertex.name_upper + 'To' + self.target_vertex.name_upper + self.name_upper + 'EdgeProperty'

    def has_properties(self) -> bool:
        return len(self.properties) > 0

    def is_recursive(self) -> bool:
        return self.source_vertex == self.target_vertex
