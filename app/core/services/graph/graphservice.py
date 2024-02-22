from app.core.entities import Graph
from app.core.repositories import IGraphRepository
from app.core.services.graph.graphserviceinterface import IGraphService


class GraphService(IGraphService):
    def __init__(self, repository: IGraphRepository):
        self.repository = repository

    def get_graph(self, project_id: str) -> Graph:
        graph = self.repository.get_graph(project_id)

        return graph
