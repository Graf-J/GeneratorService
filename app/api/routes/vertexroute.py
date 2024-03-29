from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_vertex_service
from app.api.dto import VertexResponseDto, VertexRequestDto
from app.core.exceptions import ProjectNotFoundException, VertexNotFoundException, VertexException
from app.core.services import IVertexService
from app.mappers import VertexMapper

router = APIRouter(
    prefix="/projects/{project_id}/vertices",
    tags=["Vertex"]
)


@router.get('/')
def get_vertices(
        project_id: str,
        service: IVertexService = Depends(get_vertex_service)
) -> List[VertexResponseDto]:
    try:
        vertices = service.get_vertices(project_id)

        return [VertexMapper.to_dto(vertex) for vertex in vertices]
    except ProjectNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{'msg': ex.message}])


@router.get('/{vertex_id}')
def get_vertex(
        project_id: str,
        vertex_id: str,
        service: IVertexService = Depends(get_vertex_service)
) -> VertexResponseDto:
    try:
        vertex = service.get_vertex(project_id, vertex_id)

        output = VertexMapper.to_dto(vertex)
        return output
    except ProjectNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{'msg': ex.message}])
    except VertexNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{'msg': ex.message}])


@router.post('/')
def create_vertex(
        vertex_request_dto: VertexRequestDto,
        project_id: str,
        service: IVertexService = Depends(get_vertex_service)
) -> VertexResponseDto:
    try:
        vertex = service.create_vertex(project_id, VertexMapper.to_entity(vertex_request_dto))

        return VertexMapper.to_dto(vertex)
    except ProjectNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{'msg': ex.message}])
    except VertexException as ex:
        raise HTTPException(status_code=ex.status_code, detail=[{'msg': ex.message, 'loc': ['body', ex.loc]}])


@router.put('/{vertex_id}')
def update_vertex(
        vertex_request_dto: VertexRequestDto,
        project_id: str,
        vertex_id: str,
        service: IVertexService = Depends(get_vertex_service)
) -> VertexResponseDto:
    try:
        vertex = service.update_vertex(project_id, vertex_id, VertexMapper.to_entity(vertex_request_dto))

        return VertexMapper.to_dto(vertex)
    except ProjectNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{'msg': ex.message}])
    except VertexNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{'msg': ex.message}])
    except VertexException as ex:
        raise HTTPException(status_code=ex.status_code, detail=[{'msg': ex.message, 'loc': ['body', ex.loc]}])


@router.delete('/{vertex_id}')
def delete_vertex(
        project_id: str,
        vertex_id: str,
        service: IVertexService = Depends(get_vertex_service)
):
    try:
        service.delete_vertex(project_id, vertex_id)
    except ProjectNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{'msg': ex.message}])
    except VertexNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{'msg': ex.message}])
