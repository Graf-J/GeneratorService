from typing import Tuple, List

from graphql import ObjectFieldNode, ObjectValueNode

from querybuilder.arguments.argument import Argument
from querybuilder.arguments.logic import Logic
from querybuilder.arguments.logicunit import LogicUnit
from querybuilder.arguments.order import Order
from querybuilder.arguments.orderdirection import OrderDirection
from querybuilder.arguments.pagination import Pagination


class ArgumentBuilder:
    def __init__(self):
        self.arguments = dict()

    def add_pagination(self, field_nodes: Tuple[ObjectFieldNode]):
        if field_nodes[0].name.value == 'offset':
            offset = int(field_nodes[0].value.value)
            if offset < 0:
                raise Exception('Offset cannot be negative')
            limit = int(field_nodes[1].value.value)
            if limit < 0:
                raise Exception('Limit cannot be negative')

            pagination_argument = Pagination(offset=offset, limit=limit)
        else:
            offset = int(field_nodes[1].value.value)
            if offset < 0:
                raise Exception('Offset cannot be negative')
            limit = int(field_nodes[0].value.value)
            if limit < 0:
                raise Exception('Limit cannot be negative')

            pagination_argument = Pagination(offset=offset, limit=limit)

        self.arguments[Argument.PAGINATION] = pagination_argument

    def add_vertex_order(self, value_nodes: Tuple[ObjectValueNode]):
        order_arguments = self.extract_order(value_nodes)

        self.arguments[Argument.VERTEX_ORDER] = order_arguments

    def add_edge_order(self, value_nodes: Tuple[ObjectValueNode]):
        order_arguments = self.extract_order(value_nodes)

        self.arguments[Argument.EDGE_ORDER] = order_arguments

    def extract_order(self, value_nodes: Tuple[ObjectValueNode]) -> List[Order]:
        order_arguments: List[Order] = []

        for value_node in value_nodes:
            if value_node.fields[0].name.value == 'property':
                order_argument = Order(
                    prop=value_node.fields[0].value.value,
                    order=OrderDirection.ASC if value_node.fields[
                                                    1].value.value == OrderDirection.ASC.value else OrderDirection.DESC
                )
            else:
                order_argument = Order(
                    prop=value_node.fields[1].value.value,
                    order=OrderDirection.ASC if value_node.fields[
                                                    0].value.value == OrderDirection.ASC.value else OrderDirection.DESC
                )
            order_arguments.append(order_argument)

        return order_arguments

    def add_vertex_logic(self, object_node: ObjectValueNode):
        logic_argument, argument_found = self.extract_logic(object_node)

        if not argument_found:
            raise Exception('In a Where clause at least one Argument has to be specified')

        self.arguments[Argument.VERTEX_LOGIC] = logic_argument

    def add_edge_logic(self, object_node: ObjectValueNode):
        logic_argument, argument_found = self.extract_logic(object_node)

        if not argument_found:
            raise Exception('In a Where clause at least one Argument has to be specified')

        self.arguments[Argument.EDGE_LOGIC] = logic_argument

    def extract_logic(self, object_node: ObjectValueNode) -> Tuple[Logic, bool]:
        logic = Logic()
        argument_found = False

        for field_node in object_node.fields:
            if field_node.name.value == 'AND':
                # If Logic passed as Object instead of List, return single Element as List
                values = [field_node.value] if field_node.value.kind == 'object_value' else field_node.value.values
                results = [self.extract_logic(obj_node) for obj_node in values]

                logic.AND = [result[0] for result in results]
                argument_found = any([result[1] for result in results])
            elif field_node.name.value == 'OR':
                # If Logic passed as Object instead of List, return single Element as List
                values = [field_node.value] if field_node.value.kind == 'object_value' else field_node.value.values
                results = [self.extract_logic(obj_node) for obj_node in values]

                logic.OR = [result[0] for result in results]
                argument_found = any([result[1] for result in results])
            else:
                # Extract info from Logic Parameter
                splitted = field_node.name.value.split('_')
                operation = splitted.pop()
                prop = '_'.join(splitted)
                # Cast Parameter into correct Datatype
                if field_node.value.kind == 'string_value':
                    value = str(field_node.value.value)
                elif field_node.value.kind == 'int_value':
                    value = int(field_node.value.value)
                elif field_node.value.kind == 'float_value':
                    value = float(field_node.value.value)
                elif field_node.value.kind == 'boolean_value':
                    value = bool(field_node.value.value)
                elif field_node.value.kind == 'null_value':
                    value = None
                else:
                    raise Exception(f"Unknown datatype '{field_node.value.kind}'")
                # Assign Parameter to correct Operation
                if operation == 'EQ':
                    argument_found = True
                    logic.EQ = LogicUnit(prop=prop, value=value)
                elif operation == 'NEQ':
                    argument_found = True
                    logic.NEQ = LogicUnit(prop=prop, value=value)
                elif operation == 'GT':
                    argument_found = True
                    logic.GT = LogicUnit(prop=prop, value=value)
                elif operation == 'GTE':
                    argument_found = True
                    logic.GTE = LogicUnit(prop=prop, value=value)
                elif operation == 'LT':
                    argument_found = True
                    logic.LT = LogicUnit(prop=prop, value=value)
                elif operation == 'LTE':
                    argument_found = True
                    logic.LTE = LogicUnit(prop=prop, value=value)
                else:
                    raise Exception(f'Unknown operation: {operation}')

        return logic, argument_found

    def build(self) -> dict:
        return self.arguments
