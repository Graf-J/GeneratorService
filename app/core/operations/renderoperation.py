from uuid import uuid4

from jinja2 import Template

from app.core.entities import Graph, Build
from app.core.valueobjects import File


class RenderOperation:
    @staticmethod
    def render_schema(template: Template, graph: Graph) -> File:
        schema = template.render(graph=graph)

        file = File(
            file_name='schema.py',
            byte_content=schema.encode('utf-8')
        )

        return file

    @staticmethod
    def render_app(template: Template, graph: Graph, port: int) -> File:
        app = template.render(graph=graph, port=port)

        file = File(
            file_name='app.py',
            byte_content=app.encode('utf-8')
        )

        return file

    @staticmethod
    def render_docker_compose(template: Template, build_config: Build) -> File:
        docker_compose = template.render(build_config=build_config, random_id=str(uuid4()))

        file = File(
            file_name='docker-compose.yaml',
            byte_content=docker_compose.encode('utf-8')
        )

        return file
