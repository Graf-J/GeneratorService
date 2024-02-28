from typing import List, Tuple

from graph.edge import Edge
from graph.vertex import Vertex
from graphql.type.definition import GraphQLResolveInfo, FieldNode
from gremlin_python.process.graph_traversal import GraphTraversalSource, GraphTraversal
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.traversal import Order as GremlinOrder
from gremlin_python.process.traversal import P
from querybuilder.arguments import ArgumentDirector, Order, OrderDirection, Argument, Pagination, Logic
from querybuilder.stack import Stack
from querybuilder.utils import manipulate_graphql_context


class QueryBuilder:
    def __init__(self, vertex: Vertex):
        self.vertex_stack = Stack[Vertex]()
        self.edge_stack = Stack[Edge]()
        # Push initial Vertex on Stack
        self.vertex_stack.push(vertex)

    def build_single_entity_query(self, g: GraphTraversalSource, info: GraphQLResolveInfo, id: str) -> GraphTraversal:
        # Extract Infos from GraphQL Tree
        manipulate_graphql_context(info)
        selections = info.field_nodes[0].selection_set.selections
        fields = [selection.name.value for selection in selections]

        # Build Query
        traversal = g.V(id).has_label(self.vertex_stack.peek().label).project(*fields)
        self.apply_vertex_projection(traversal, selections, fields)

        return traversal

    def build_multiple_entities_query(self, g: GraphTraversalSource, info: GraphQLResolveInfo) -> GraphTraversal:
        # Extract Infos from GraphQL Tree
        manipulate_graphql_context(info)
        selections = info.field_nodes[0].selection_set.selections
        fields = [selection.name.value for selection in selections]

        # Extract Arguments from GraphQL-Query
        arguments = ArgumentDirector.construct(info.field_nodes[0].arguments)

        # Build Query
        traversal = g.V().has_label(self.vertex_stack.peek().label)

        # Apply Logic if specified in GraphQL-Query
        if Argument.VERTEX_LOGIC in arguments:
            self.apply_logic(traversal, arguments[Argument.VERTEX_LOGIC])

        # Apply Fields of GraphQL-Query in Germlin-Projection
        traversal.project(*fields)
        self.apply_vertex_projection(traversal, selections, fields)

        # Apply Order By if specified in GraphQL-Query
        if Argument.VERTEX_ORDER in arguments:
            self.apply_order_by(traversal, arguments[Argument.VERTEX_ORDER])

        # Apply Pagination if specified in GraphQL-Query
        if Argument.PAGINATION in arguments:
            self.apply_pagination(traversal, arguments[Argument.PAGINATION])

        return traversal

    def apply_vertex_projection(self, traversal: GraphTraversal, selections: Tuple[FieldNode], fields: List[str]):
        for idx, field in enumerate(fields):
            # Check if Field is the id
            if field == 'id':
                traversal.by(__.id_())
                continue
            # Check if Field is the Label
            if field == 'label':
                traversal.by(__.label())
                continue
            # Check if Field is a Property
            if field in [prop.field_name for prop in self.vertex_stack.peek().properties]:
                traversal.by(__.coalesce(__.values(field), __.constant(None)))
                continue
            # Check if Field is an outgoing Edge
            out_edge = self.vertex_stack.peek().find_out_edge_by_field_name(field)
            if out_edge is not None:
                # Push Out-Edge on Stack
                self.edge_stack.push(out_edge)
                # Extract Arguments from GraphQL-Query
                arguments = ArgumentDirector.construct(selections[idx].arguments)
                # Build Query
                out_edge_query = self.generate_out_edge_query(selections[idx].selection_set.selections, arguments)
                # Apply Edge Order By if specified in GraphQL-Query
                if Argument.EDGE_ORDER in arguments:
                    self.apply_order_by(out_edge_query, arguments[Argument.EDGE_ORDER])
                # Apply Pagination if specified in GraphQL-Query
                if Argument.PAGINATION in arguments:
                    self.apply_pagination(out_edge_query, arguments[Argument.PAGINATION])
                # Convert to List using fold
                traversal.by(out_edge_query.fold())
                # Pop Out-Edge from Stack
                self.edge_stack.pop()
                continue
            # Check if Field is an incoming Edge
            in_edge = self.vertex_stack.peek().find_in_edge_by_field_name(field)
            if in_edge is not None:
                # Push In-Edge on Stack
                self.edge_stack.push(in_edge)
                # Extract Arguments from GraphQL-Query
                arguments = ArgumentDirector.construct(selections[idx].arguments)
                # Build Query
                in_edge_query = self.generate_in_edge_query(selections[idx].selection_set.selections, arguments)
                # Apply Edge Order By if specified in GraphQL-Query
                if Argument.EDGE_ORDER in arguments:
                    self.apply_order_by(in_edge_query, arguments[Argument.EDGE_ORDER])
                # Apply Pagination if specified in GraphQL-Query
                if Argument.PAGINATION in arguments:
                    self.apply_pagination(in_edge_query, arguments[Argument.PAGINATION])
                # Convert to List using fold
                traversal.by(in_edge_query.fold())
                # Pop In-Edge from Stack
                self.edge_stack.pop()
                continue

            raise Exception(f"Unknown field: '{field}'")

    def generate_out_edge_query(self, selections: Tuple[FieldNode], arguments: dict) -> GraphTraversal:
        # Extract Infos from GraphQL Tree
        fields = [selection.name.value for selection in selections]

        # Build Query
        traversal = __.out_e(self.edge_stack.peek().label)

        # Apply Edge-Logic if specified in GraphQL-Query
        if Argument.EDGE_LOGIC in arguments:
            self.apply_logic(traversal, arguments[Argument.EDGE_LOGIC])

        # Apply Vertex-Logic if specified in GraphQL-Query
        if Argument.VERTEX_LOGIC in arguments:
            vertex_logic_traversal = __.in_v().has_label(self.edge_stack.peek().target_vertex.label)
            self.apply_logic(vertex_logic_traversal, arguments[Argument.VERTEX_LOGIC])
            traversal.where(vertex_logic_traversal)

        # Apply Vertex-Order if specified in GraphQL-Query
        if Argument.VERTEX_ORDER in arguments:
            target_vertex_label = self.edge_stack.peek().target_vertex.label
            self.apply_order_by_in_vertex(traversal, arguments[Argument.VERTEX_ORDER], target_vertex_label)

        # Apply Fields of GraphQL-Query in Germlin-Projection
        traversal.project(*fields)
        self.apply_edge_projection(traversal, selections, fields, out_edge=True)

        return traversal

    def generate_in_edge_query(self, selections: Tuple[FieldNode], arguments: dict) -> GraphTraversal:
        # Extract Infos from GraphQL Tree
        fields = [selection.name.value for selection in selections]

        # Build Query
        traversal = __.in_e(self.edge_stack.peek().label)

        # Apply Edge-Logic if specified in GraphQL-Query
        if Argument.EDGE_LOGIC in arguments:
            self.apply_logic(traversal, arguments[Argument.EDGE_LOGIC])

        # Apply Vertex-Logic if specified in GraphQL-Query
        if Argument.VERTEX_LOGIC in arguments:
            vertex_logic_traversal = __.out_v().has_label(self.edge_stack.peek().source_vertex.label)
            self.apply_logic(vertex_logic_traversal, arguments[Argument.VERTEX_LOGIC])
            traversal.where(vertex_logic_traversal)

        # Apply Vertex-Order if specified in GraphQL-Query
        if Argument.VERTEX_ORDER in arguments:
            source_vertex_label = self.edge_stack.peek().source_vertex.label
            self.apply_order_by_out_vertex(traversal, arguments[Argument.VERTEX_ORDER], source_vertex_label)

        # Apply Fields of GraphQL-Query in Germlin-Projection
        traversal.project(*fields)
        self.apply_edge_projection(traversal, selections, fields, out_edge=False)

        return traversal

    def apply_edge_projection(self, traversal: GraphTraversal, selections: Tuple[FieldNode],
                              fields: List[str], out_edge: bool):
        for idx, field in enumerate(fields):
            # Check if Field is the id
            if field == 'id':
                traversal.by(__.id_())
                continue
            # Check if Field is the label
            if field == 'label':
                traversal.by(__.label())
                continue
            # Check if Field is a Property
            if field in [prop.field_name for prop in self.edge_stack.peek().properties]:
                traversal.by(__.coalesce(__.values(field), __.constant(None)))
                continue
            # Check if Field-Name of Target-Vertex of outgoing Edge matches the Field-Name of GraphQL Field
            target_vertex = self.edge_stack.peek().target_vertex
            if field == target_vertex.field_name and out_edge:
                # Push Target-Vertex on Stack
                self.vertex_stack.push(target_vertex)
                # Build Query
                in_vertex_query = self.generate_in_vertex_query(selections[idx].selection_set.selections)
                traversal.by(in_vertex_query)
                # Pop Target-Vertex from Stack
                self.vertex_stack.pop()
                continue
            # Check if Field-Name of Source-Vertex of incoming Edge matches the Field-Name of GraphQL Field
            source_vertex = self.edge_stack.peek().source_vertex
            if field == source_vertex.field_name and not out_edge:
                # Push Source-Vertex on Stack
                self.vertex_stack.push(source_vertex)
                # Build Query
                out_vertex_query = self.generate_out_vertex_query(selections[idx].selection_set.selections)
                traversal.by(out_vertex_query)
                # Pop Source-Vertex from Stack
                self.vertex_stack.pop()
                continue

            raise Exception(f"Unknown field: '{field}'")

    def generate_out_vertex_query(self, selections: Tuple[FieldNode]) -> GraphTraversal:
        # Extract Infos from GraphQL Tree
        fields = [selection.name.value for selection in selections]

        # Build Query
        traversal = __.out_v().hasLabel(self.vertex_stack.peek().label).project(*fields)
        self.apply_vertex_projection(traversal, selections, fields)

        return traversal

    def generate_in_vertex_query(self, selections: Tuple[FieldNode]) -> GraphTraversal:
        # Extract Infos from GraphQL Tree
        fields = [selection.name.value for selection in selections]

        # Build Query
        traversal = __.in_v().has_label(self.vertex_stack.peek().label).project(*fields)
        self.apply_vertex_projection(traversal, selections, fields)

        return traversal

    def apply_order_by(self, traversal: GraphTraversal, order_arguments: List[Order]):
        traversal.order()
        for order_argument in order_arguments:
            order_direction = GremlinOrder.asc if order_argument.order == OrderDirection.ASC else GremlinOrder.desc
            traversal.by(order_argument.property, order_direction)

    def apply_order_by_in_vertex(self, traversal: GraphTraversal, order_arguments: List[Order], vertex_label: str):
        traversal.order()
        for order_argument in order_arguments:
            order_direction = GremlinOrder.asc if order_argument.order == OrderDirection.ASC else GremlinOrder.desc
            traversal.by(__.in_v().has_label(vertex_label).values(order_argument.property), order_direction)

    def apply_order_by_out_vertex(self, traversal: GraphTraversal, order_arguments: List[Order], vertex_label: str):
        traversal.order()
        for order_argument in order_arguments:
            order_direction = GremlinOrder.asc if order_argument.order == OrderDirection.ASC else GremlinOrder.desc
            traversal.by(__.out_v().has_label(vertex_label).values(order_argument.property), order_direction)

    def apply_pagination(self, traversal: GraphTraversal, pagination_argument: Pagination):
        traversal.skip(pagination_argument.offset).limit(pagination_argument.limit)

    def apply_logic(self, traversal: GraphTraversal, logic_argument: Logic):
        logic_params = self.extract_logic_params(logic_argument)
        traversal.and_(*logic_params)

    def extract_logic_params(self, logic_argument: Logic) -> list:
        logic_params = []

        if logic_argument.EQ is not None:
            logic_params.append(__.has(logic_argument.EQ.property, P.eq(logic_argument.EQ.value)))
        if logic_argument.NEQ is not None:
            logic_params.append(__.has(logic_argument.NEQ.property, P.neq(logic_argument.NEQ.value)))
        if logic_argument.GT is not None:
            logic_params.append(__.has(logic_argument.GT.property, P.gt(logic_argument.GT.value)))
        if logic_argument.GTE is not None:
            logic_params.append(__.has(logic_argument.GTE.property, P.gte(logic_argument.GTE.value)))
        if logic_argument.LT is not None:
            logic_params.append(__.has(logic_argument.LT.property, P.lt(logic_argument.LT.value)))
        if logic_argument.LTE is not None:
            logic_params.append(__.has(logic_argument.LTE.property, P.lte(logic_argument.LTE.value)))
        if logic_argument.AND is not None:
            and_params = []
            for logic in logic_argument.AND:
                params = self.extract_logic_params(logic)
                and_params.extend(params)

            logic_params.append(__.and_(*and_params))
        if logic_argument.OR is not None:
            or_params = []
            for logic in logic_argument.OR:
                params = self.extract_logic_params(logic)
                or_params.extend(params)

            logic_params.append(__.or_(*or_params))

        return logic_params
