import uuid
from typing import List
from fastapi import APIRouter, Depends
from app.api.dependencies import get_vertex_service
from app.api.dto import VertexResponseDto, VertexRequestDto
from app.core.services import IVertexService
from app.core.entities import Vertex, Property
from app.mappers import VertexMapper

router = APIRouter(
    prefix="/projects/{project_id}/vertex",
    tags=["Vertex"]
)


@router.get('/')
async def get_vertices(
        project_id: str,
        service: IVertexService = Depends(get_vertex_service)
) -> List[VertexResponseDto]:
    print(project_id)
    vertices = service.get_vertices()

    data = {
        "_id": uuid.uuid4(),
        "name": "string",
        "position_x": 0,
        "position_y": 0,
        "radius": 0,
        "properties": [
            Property('hello', True, 'String')
        ],
    }

    mock_vertex = Vertex(**data)

    return [VertexMapper.to_dto(mock_vertex)]


@router.post('/')
async def create_vertex(vertex_request_dto: VertexRequestDto, service: IVertexService = Depends(get_vertex_service)):
    vertex = service.create_vertex(VertexMapper.to_entity(vertex_request_dto))

    # TODO: Check for DuplicateException
    return 'Hello'
