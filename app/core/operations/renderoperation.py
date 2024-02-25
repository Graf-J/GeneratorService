from jinja2 import Template

from app.core.entities import Graph
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
    def render_app(template: Template, graph: Graph) -> File:
        app = template.render(graph=graph)

        file = File(
            file_name='app.py',
            byte_content=app.encode('utf-8')
        )

        return file
