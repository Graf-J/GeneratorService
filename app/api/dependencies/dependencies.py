from fastapi import Depends

from app.core.repositories import (
    IVertexRepository,
    VertexRepository,
    IEdgeRepository,
    EdgeRepository,
    IProjectRepository,
    ProjectRepository
)
from app.core.services import (
    IVertexService,
    VertexService,
    IEdgeService,
    EdgeService,
    IProjectService,
    ProjectService
)
from app.infrastructure.storage import (
    IStorage,
    PickleStorage
)
from app.infrastructure.utils import FileManager


# Other
def get_filemanager() -> FileManager:
    return FileManager()


# Storage
def get_graph_storage(filemanager: FileManager = Depends(get_filemanager)) -> IStorage:
    return PickleStorage(filemanager)


# Repositories
def get_vertex_repository(graph_storage: IStorage = Depends(get_graph_storage)) -> IVertexRepository:
    return VertexRepository(graph_storage)


def get_edge_repository(graph_storage: IStorage = Depends(get_graph_storage)) -> IEdgeRepository:
    return EdgeRepository(graph_storage)


def get_project_repository(graph_storage: IStorage = Depends(get_graph_storage)) -> IProjectRepository:
    return ProjectRepository(graph_storage)


# Services
def get_vertex_service(vertex_repository: IVertexRepository = Depends(get_vertex_repository)) -> IVertexService:
    return VertexService(vertex_repository)


def get_edge_service(edge_repository: IEdgeRepository = Depends(get_edge_repository)) -> IEdgeService:
    return EdgeService(edge_repository)


def get_project_service(project_repository: IProjectRepository = Depends(get_project_repository)) -> IProjectService:
    return ProjectService(project_repository)
