from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_vertex_service
from app.api.dto import VertexResponseDto, VertexRequestDto
from app.core.exceptions import DuplicateException
from app.core.exceptions import NotFoundException
from app.core.services import IVertexService
from app.mappers import VertexMapper

router = APIRouter(
    prefix="/projects/{project_id}/vertices",
    tags=["Vertex"]
)


@router.get('/')
async def get_vertices(
        project_id: str,
        service: IVertexService = Depends(get_vertex_service)
) -> List[VertexResponseDto]:
    try:
        vertices = service.get_vertices(project_id)

        return [VertexMapper.to_dto(vertex) for vertex in vertices]
    except NotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{'msg': ex.message}])


@router.get('/{vertex_id}')
async def get_vertex(
        project_id: str,
        vertex_id: str,
        service: IVertexService = Depends(get_vertex_service)
) -> VertexRequestDto:
    try:
        vertex = service.get_vertex(project_id, vertex_id)

        return VertexMapper.to_dto(vertex)
    except NotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{'msg': ex.message}])


@router.post('/')
async def create_vertex(
        vertex_request_dto: VertexRequestDto,
        project_id: str,
        service: IVertexService = Depends(get_vertex_service)
) -> VertexResponseDto:
    try:
        vertex = service.create_vertex(project_id, VertexMapper.to_entity(vertex_request_dto))

        return VertexMapper.to_dto(vertex)
    except NotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{'msg': ex.message}])
    except DuplicateException as ex:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=[{'msg': ex.message}])
