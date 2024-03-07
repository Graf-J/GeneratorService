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
    OutputRepository,
    ITemplateRepository,
    TemplateRepository
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
    OutputFolderAdapter,
    TemplateFolderAdapter
)
from app.infrastructure.storages import (
    IProjectStorage,
    PickleProjectStorage,
    IOutputStorage,
    OutputStorage,
    ITemplateStorage,
    TemplateStorage
)


# Adapters
def get_project_folder_adapter() -> ProjectFolderAdapter:
    return ProjectFolderAdapter()


def get_output_folder_adapter() -> OutputFolderAdapter:
    return OutputFolderAdapter()


def get_template_folder_adapter() -> TemplateFolderAdapter:
    return TemplateFolderAdapter()


# Storage
def get_project_storage(
        project_folder_adapter: ProjectFolderAdapter = Depends(get_project_folder_adapter)) -> IProjectStorage:
    return PickleProjectStorage(project_folder_adapter)


def get_output_storage(
        output_folder_adapter: OutputFolderAdapter = Depends(get_output_folder_adapter)) -> IOutputStorage:
    return OutputStorage(output_folder_adapter)


def get_template_storage(
        template_folder_adapter: TemplateFolderAdapter = Depends(get_template_folder_adapter)) -> ITemplateStorage:
    return TemplateStorage(template_folder_adapter)


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


def get_template_repository(template_storage: ITemplateStorage = Depends(get_template_storage)) -> ITemplateRepository:
    return TemplateRepository(template_storage)


# Services
def get_vertex_service(vertex_repository: IVertexRepository = Depends(get_vertex_repository)) -> IVertexService:
    return VertexService(vertex_repository)


def get_edge_service(edge_repository: IEdgeRepository = Depends(get_edge_repository)) -> IEdgeService:
    return EdgeService(edge_repository)


def get_project_service(
        project_repository: IProjectRepository = Depends(get_project_repository),
        output_repository: IOutputRepository = Depends(get_output_repository)
) -> IProjectService:
    return ProjectService(project_repository, output_repository)


def get_graph_service(graph_repository: IGraphRepository = Depends(get_graph_repository)) -> IGraphService:
    return GraphService(graph_repository)


def get_build_service(
        graph_repository: IGraphRepository = Depends(get_graph_repository),
        project_repository: IProjectRepository = Depends(get_project_repository),
        template_repository: ITemplateRepository = Depends(get_template_repository),
        output_repository: IOutputRepository = Depends(get_output_repository)
) -> IBuildService:
    return BuildService(graph_repository, project_repository, template_repository, output_repository)
