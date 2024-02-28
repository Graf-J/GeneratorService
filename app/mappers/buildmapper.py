from app.api.dto import BuildRequestDto
from app.core.entities import Build


class BuildMapper:
    @staticmethod
    def to_entity(dto: BuildRequestDto) -> Build:
        build = Build(
            port=dto.port,
            volume=dto.volume
        )

        return build
