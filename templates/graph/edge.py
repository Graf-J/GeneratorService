from typing import List

from graph.property import Property


class Edge:
    def __init__(
            self,
            _id: str,
            label: str,
            out_field_name: str,
            in_field_name: str,
            source_vertex_id: str,
            target_vertex_id: str,
            multi_edge: bool,
            properties: List[Property]
    ):
        self.id = _id
        self.label = label
        self.out_field_name = out_field_name
        self.in_field_name = in_field_name
        self.source_vertex_id = source_vertex_id
        self.target_vertex_id = target_vertex_id
        self.multi_edge = multi_edge
        self.properties = properties

        self.source_vertex = None
        self.target_vertex = None
