from fastapi import APIRouter, HTTPException, status, Depends

from app.api.dependencies import get_graph_service
from app.api.dto import GraphResponseDto
from app.core.exceptions import ProjectNotFoundException
from app.core.services import IGraphService
from app.mappers import GraphMapper

router = APIRouter(
    prefix="/projects/{project_id}/graph",
    tags=["Graph"]
)


@router.get('/')
def get_graph(project_id: str, service: IGraphService = Depends(get_graph_service)) -> GraphResponseDto:
    try:
        graph = service.get_graph(project_id)

        return GraphMapper.to_dto(graph)
    except ProjectNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{'msg': ex.message}])
