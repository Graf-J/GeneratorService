from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_edge_service
from app.api.dto import EdgeRequestDto, EdgeResponseDto
from app.core.exceptions import ProjectNotFoundException, VertexNotFoundException, EdgeNotFoundException, EdgeException
from app.core.services import IEdgeService
from app.mappers import EdgeMapper

router = APIRouter(
    prefix="/projects/{project_id}/edges",
    tags=["Edge"]
)


@router.get('/')
async def get_edges(
        project_id: str,
        edge_service: IEdgeService = Depends(get_edge_service)
) -> List[EdgeResponseDto]:
    try:
        edges = edge_service.get_edges(project_id)

        return [EdgeMapper.to_dto(edge) for edge in edges]
    except ProjectNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{'msg': ex.message}])


@router.get('/{edge_id}')
async def get_edge(
        project_id: str,
        edge_id: str,
        edge_service: IEdgeService = Depends(get_edge_service)
) -> EdgeResponseDto:
    try:
        edge = edge_service.get_edge(project_id, edge_id)

        return EdgeMapper.to_dto(edge)
    except ProjectNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{'msg': ex.message}])
    except EdgeNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{'msg': ex.message}])


@router.post('/')
async def create_edge(
        edge_request_dto: EdgeRequestDto,
        project_id: str,
        edge_service: IEdgeService = Depends(get_edge_service)
) -> EdgeResponseDto:
    try:
        edge = edge_service.create_edge(
            project_id,
            EdgeMapper.to_entity(edge_request_dto),
            str(edge_request_dto.source_vertex_id),
            str(edge_request_dto.target_vertex_id)
        )

        return EdgeMapper.to_dto(edge)
    except ProjectNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{'msg': ex.message}])
    except VertexNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{'msg': ex.message}])
    except EdgeException as ex:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=[{'msg': ex.message}])
