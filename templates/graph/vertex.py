from typing import List
from graph.property import Property
from graph.edge import Edge


class Vertex:
    def __init__(
            self,
            _id: str,
            label: str,
            single_field_name: str,
            multiple_field_name: str,
            properties: List[Property]
    ):
        self.id = _id
        self.label = label
        self.single_field_name = single_field_name
        self.multiple_field_name = multiple_field_name
        self.properties = properties

        self.out_edges: List[Edge] = []
        self.in_edges: List[Edge] = []

    def find_out_edge_by_field_name(self, field_name: str) -> Edge | None:
        for edge in self.out_edges:
            if field_name == edge.out_field_name:
                return edge

        return None

    def find_in_edge_by_field_name(self, field_name: str) -> Edge | None:
        for edge in self.in_edges:
            if field_name == edge.in_field_name:
                return edge

        return None
