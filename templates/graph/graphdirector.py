from graph.graph import Graph
from graph.graphbuilder import GraphBuilder
from graph.vertex import Vertex
from graph.edge import Edge
from graph.property import Property


class GraphDirector:
    @staticmethod
    def construct(graph_dict: dict) -> Graph:
        builder = GraphBuilder()

        for vertex in graph_dict['vertices']:
            builder.add_vertex(
                Vertex(
                    _id=vertex['id'],
                    label=vertex['label'],
                    single_field_name=vertex['single_field_name'],
                    multiple_field_name=vertex['multiple_field_name'],
                    properties=[Property(field_name=prop['field_name']) for prop in vertex['properties']]
                )
            )

        for edge in graph_dict['edges']:
            builder.add_edge(
                Edge(
                    label=edge['label'],
                    out_field_name=edge['out_field_name'],
                    in_field_name=edge['in_field_name'],
                    source_vertex_id=edge['source_vertex_id'],
                    target_vertex_id=edge['target_vertex_id'],
                    multi_edge=edge['multi_edge'],
                    properties=[Property(field_name=prop['field_name']) for prop in edge['properties']]
                )
            )

        graph = builder.build()
        return graph

