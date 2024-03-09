import uuid
from typing import List

from app.api.dto import VertexRequestDto, VertexResponseDto, PropertyDto
from app.core.entities import Vertex, Property
from app.mappers.edgemapper import EdgeMapper
from app.mappers.mapper import Mapper


class VertexMapper(Mapper):
    @staticmethod
    def to_entity(dto: VertexRequestDto) -> Vertex:
        properties: List[Property] = []
        for prop in dto.properties:
            properties.append(Property(key=prop.key, required=prop.required, datatype=prop.datatype))

        vertex_entity = Vertex(
            _id=str(uuid.uuid4()),
            name=dto.name,
            position_x=dto.position_x,
            position_y=dto.position_y,
            properties=properties
        )

        return vertex_entity

    @staticmethod
    def to_dto(entity: Vertex) -> VertexResponseDto:
        properties: List[PropertyDto] = []
        for prop in entity.properties:
            properties.append(PropertyDto(key=prop.key, required=prop.required, datatype=prop.datatype))

        vertex_dto = VertexResponseDto(
            id=entity.id,
            name=entity.name,
            position_x=entity.position_x,
            position_y=entity.position_y,
            properties=properties,
            out_edges=[EdgeMapper.to_dto(out_edge) for out_edge in entity.out_edges],
            in_edges=[EdgeMapper.to_dto(in_edge) for in_edge in entity.in_edges]
        )

        return vertex_dto
