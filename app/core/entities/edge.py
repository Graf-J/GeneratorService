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
    def manipulate_input_name(self) -> str:
        return self.source_vertex.name_upper + 'To' + self.target_vertex.name_upper + 'Via' + self.name_upper + 'EdgeInput'

    @property
    def property_name(self) -> str:
        return self.source_vertex.name_upper + 'To' + self.target_vertex.name_upper + self.name_upper + 'EdgeProperty'

    def has_properties(self) -> bool:
        return len(self.properties) > 0

    def is_recursive(self) -> bool:
        return self.source_vertex == self.target_vertex

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'label': self.name,
            'out_field_name': self.out_field_name,
            'in_field_name': self.in_field_name,
            'source_vertex_id': self.source_vertex.id,
            'target_vertex_id': self.target_vertex.id,
            'multi_edge': self.multi_edge,
            'properties': [prop.to_dict() for prop in self.properties]
        }
