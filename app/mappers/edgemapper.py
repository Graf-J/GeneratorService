import uuid
from typing import List

from app.api.dto import EdgeRequestDto, EdgeResponseDto, PropertyDto
from app.core.entities import Edge, Property
from app.mappers.mapper import Mapper


class EdgeMapper(Mapper):
    @staticmethod
    def to_entity(dto: EdgeRequestDto) -> Edge:
        properties: List[Property] = []
        for prop in dto.properties:
            properties.append(Property(key=prop.key, required=prop.required, datatype=prop.datatype))

        edge_entity = Edge(
            _id=str(uuid.uuid4()),
            name=dto.name,
            properties=properties
        )

        return edge_entity

    @staticmethod
    def to_dto(entity: Edge) -> EdgeResponseDto:
        properties: List[PropertyDto] = []
        for prop in entity.properties:
            properties.append(PropertyDto(key=prop.key, required=prop.required, datatype=prop.datatype))

        edge_dto = EdgeResponseDto(
            id=entity.id,
            name=entity.name,
            properties=properties,
            source_vertex_id=entity.source_vertex.id,
            target_vertex_id=entity.target_vertex.id
        )

        return edge_dto
