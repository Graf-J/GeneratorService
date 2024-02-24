from jinja2 import Template

from app.core.entities import Graph


class SchemaOperation:
    @staticmethod
    def render_schema(template: Template, graph: Graph):
        schema = template.render(graph=graph)

        return schema
