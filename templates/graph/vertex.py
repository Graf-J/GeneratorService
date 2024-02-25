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
