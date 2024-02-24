from fastapi import Depends

from app.core.repositories import (
    IVertexRepository,
    VertexRepository,
    IEdgeRepository,
    EdgeRepository,
    IProjectRepository,
    ProjectRepository,
    IGraphRepository,
    GraphRepository,
    IOutputRepository,
    OutputRepository
)
from app.core.services import (
    IVertexService,
    VertexService,
    IEdgeService,
    EdgeService,
    IProjectService,
    ProjectService,
    IGraphService,
    GraphService,
    IBuildService,
    BuildService
)
from app.infrastructure.adapters import (
    ProjectFolderAdapter,
    OutputFolderAdapter
)
from app.infrastructure.storages import (
    IProjectStorage,
    PickleProjectStorage,
    IOutputStorage,
    OutputStorage
)


# Adapters
def get_project_folder_adapter() -> ProjectFolderAdapter:
    return ProjectFolderAdapter()


def get_output_folder_adapter() -> OutputFolderAdapter:
    return OutputFolderAdapter()


# Storage
def get_project_storage(
        project_folder_adapter: ProjectFolderAdapter = Depends(get_project_folder_adapter)) -> IProjectStorage:
    return PickleProjectStorage(project_folder_adapter)


def get_output_storage(
        output_folder_adapter: OutputFolderAdapter = Depends(get_output_folder_adapter)) -> IOutputStorage:
    return OutputStorage(output_folder_adapter)


# Repositories
def get_vertex_repository(project_storage: IProjectStorage = Depends(get_project_storage)) -> IVertexRepository:
    return VertexRepository(project_storage)


def get_edge_repository(project_storage: IProjectStorage = Depends(get_project_storage)) -> IEdgeRepository:
    return EdgeRepository(project_storage)


def get_project_repository(project_storage: IProjectStorage = Depends(get_project_storage)) -> IProjectRepository:
    return ProjectRepository(project_storage)


def get_graph_repository(project_storage: IProjectStorage = Depends(get_project_storage)) -> IGraphRepository:
    return GraphRepository(project_storage)


def get_output_repository(output_storage: IOutputStorage = Depends(get_output_storage)) -> IOutputRepository:
    return OutputRepository(output_storage)


# Services
def get_vertex_service(vertex_repository: IVertexRepository = Depends(get_vertex_repository)) -> IVertexService:
    return VertexService(vertex_repository)


def get_edge_service(edge_repository: IEdgeRepository = Depends(get_edge_repository)) -> IEdgeService:
    return EdgeService(edge_repository)


def get_project_service(project_repository: IProjectRepository = Depends(get_project_repository)) -> IProjectService:
    return ProjectService(project_repository)


def get_graph_service(graph_repository: IGraphRepository = Depends(get_graph_repository)) -> IGraphService:
    return GraphService(graph_repository)


def get_build_service(
        graph_repository: IGraphRepository = Depends(get_graph_repository),
        project_repository: IProjectRepository = Depends(get_project_repository),
        output_repository: IOutputRepository = Depends(get_output_repository)
) -> IBuildService:
    return BuildService(graph_repository, project_repository, output_repository)
