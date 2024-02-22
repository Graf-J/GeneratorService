from app.core.entities import Graph
from app.core.exceptions import ProjectNotFoundException
from app.core.repositories.graph.graphrepositoryinterface import IGraphRepository
from app.infrastructure.storage import IStorage


class GraphRepository(IGraphRepository):
    def __init__(self, storage: IStorage):
        self.storage = storage

    def get_graph(self, project_id: str) -> Graph:
        try:
            graph = self.storage.load_graph(project_id)

            return graph
        except ValueError as ex:
            raise ProjectNotFoundException(str(ex))
