from typing import List

from app.core.entities import Vertex
from app.core.exceptions import ProjectNotFoundException
from app.core.repositories.vertex.vertexrepositoryinterface import IVertexRepository
from app.infrastructure.storages.project.projectstorageinterface import IProjectStorage


class VertexRepository(IVertexRepository):
    def __init__(self, storage: IProjectStorage):
        self.storage = storage

    def get_vertices(self, project_id: str) -> List[Vertex]:
        try:
            graph = self.storage.load_graph(project_id)
            vertices = graph.vertices

            return vertices
        except ValueError as ex:
            raise ProjectNotFoundException(str(ex))

    def get_vertex(self, project_id: str, vertex_id: str) -> Vertex:
        try:
            graph = self.storage.load_graph(project_id)
            vertex = graph.find_vertex_by_id(vertex_id)

            return vertex
        except ValueError as ex:
            raise ProjectNotFoundException(str(ex))

    def create_vertex(self, project_id: str, vertex: Vertex) -> Vertex:
        try:
            graph = self.storage.load_graph(project_id)
            graph.add_vertex(vertex)
            self.storage.save_graph(project_id, graph)

            return vertex
        except ValueError as ex:
            raise ProjectNotFoundException(str(ex))

    def update_vertex(self, project_id: str, vertex_id: str, vertex: Vertex) -> Vertex:
        try:
            graph = self.storage.load_graph(project_id)
            updated_vertex = graph.update_vertex(vertex_id, vertex)
            self.storage.save_graph(project_id, graph)

            return updated_vertex
        except ValueError as ex:
            raise ProjectNotFoundException(str(ex))

    def delete_vertex(self, project_id: str, vertex_id: str):
        try:
            graph = self.storage.load_graph(project_id)
            graph.delete_vertex(vertex_id)
            self.storage.save_graph(project_id, graph)
        except ValueError as ex:
            raise ProjectNotFoundException(str(ex))
