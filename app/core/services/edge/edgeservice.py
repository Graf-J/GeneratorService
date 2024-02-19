from typing import List

from app.core.entities import Edge
from app.core.repositories import IEdgeRepository
from app.core.services.edge.edgeserviceinterface import IEdgeService


class EdgeService(IEdgeService):
    def __init__(self, repository: IEdgeRepository):
        self.repository = repository

    def get_edges(self, project_id: str) -> List[Edge]:
        edges = self.repository.get_edges(project_id)

        return edges

    def get_edge(self, project_id: str, edge_id: str) -> Edge:
        edge = self.repository.get_edge(project_id, edge_id)

        return edge

    def create_edge(self, project_id: str, edge: Edge, source_vertex_id: str, target_vertex_id: str) -> Edge:
        edge = self.repository.create_edge(project_id, edge, source_vertex_id, target_vertex_id)

        return edge
