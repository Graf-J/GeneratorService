from app.api.dto import GraphResponseDto
from app.core.entities import Graph
from app.mappers.edgemapper import EdgeMapper
from app.mappers.mapper import Mapper
from app.mappers.vertexmapper import VertexMapper


class GraphMapper(Mapper):
    @staticmethod
    def to_entity(dto):
        raise NotImplementedError()

    @staticmethod
    def to_dto(entity: Graph) -> GraphResponseDto:
        graph_dto = GraphResponseDto(
            vertices=[VertexMapper.to_dto(vertex) for vertex in entity.vertices],
            edges=[EdgeMapper.to_dto(edge) for edge in entity.edges]
        )

        return graph_dto
