from typing import List

from app.core.entities import Edge
from app.core.repositories.edge.edgerepositoryinterface import IEdgeRepository
from app.infrastructure.storage import IStorage


class EdgeRepository(IEdgeRepository):
    def __init__(self, storage: IStorage):
        self.storage = storage

    def get_edges(self, project_id: str) -> List[Edge]:
        graph = self.storage.load_graph(project_id)
        edges = graph.edges

        return edges

    def get_edge(self, project_id: str, edge_id: str) -> Edge:
        graph = self.storage.load_graph(project_id)
        edge = graph.find_edge_by_id(edge_id)

        return edge

    def create_edge(self, project_id: str, edge: Edge, source_vertex_id: str, target_vertex_id: str) -> Edge:
        graph = self.storage.load_graph(project_id)
        graph.add_edge(edge, source_vertex_id, target_vertex_id)
        self.storage.save_graph(project_id, graph)

        return edge
