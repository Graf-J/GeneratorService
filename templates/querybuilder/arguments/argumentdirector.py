from typing import Tuple

from graphql import ArgumentNode

from querybuilder.arguments.argument import Argument
from querybuilder.arguments.argumentbuilder import ArgumentBuilder


class ArgumentDirector:
    @staticmethod
    def construct(arguments: Tuple[ArgumentNode, ...]) -> dict:
        builder = ArgumentBuilder()

        for argument in arguments:
            if argument.name.value == Argument.PAGINATION.value:
                builder.add_pagination(argument.value.fields)

            # 'orderBy' for Top-Level Arguments in Query
            elif argument.name.value == Argument.VERTEX_ORDER.value or argument.name.value == 'orderBy':
                if argument.value.kind == 'object_value':
                    builder.add_vertex_order(tuple([argument.value]))
                else:
                    builder.add_vertex_order(argument.value.values)

            elif argument.name.value == Argument.EDGE_ORDER.value:
                if argument.value.kind == 'object_value':
                    builder.add_edge_order(tuple([argument.value]))
                else:
                    builder.add_edge_order(argument.value.values)

            # 'where' for Top-Level Arguments in Query
            elif argument.name.value == Argument.VERTEX_LOGIC.value or argument.name.value == 'where':
                builder.add_vertex_logic(argument.value)

            elif argument.name.value == Argument.EDGE_LOGIC.value:
                builder.add_edge_logic(argument.value)

            else:
                raise Exception(f"Unknown argument '{argument.name.value}'")

        return builder.build()
