from graphql import FragmentSpreadNode, DirectiveNode, VariableNode
from graphql.type.definition import GraphQLResolveInfo


def manipulate_graphql_context(info: GraphQLResolveInfo):
    """
    Takes the whole Info-Context of the GraphQL-Query, manipulates it and returns the manipulated selections.

    Parameters
    ----------
        info: GraphQLResolveInfo

    Returns
    -------
        tuple
    """
    # Replace Fragments with Fields
    info.field_nodes[0].selection_set.selections = inject_graqhql_fragments(
        info.field_nodes[0].selection_set.selections,
        {fragment_name: fragment_value.selection_set.selections for fragment_name, fragment_value in
         info.fragments.items()},
        info.variable_values
    )
    # Replace Variables with Values
    inject_graphql_variables(
        info.field_nodes,
        info.variable_values
    )

    return info


def inject_graqhql_fragments(selections: tuple, fragment_selections: dict, variables: dict) -> tuple:
    """
    Takes selections and the selections specified in the fragments stored as a key (name of the Fragment) and value (tuples of
    selections of the Fragment). It runs in a recursive approach through the whole GraphQL-Query to replace every Fragment with
    the according Fields.
    Since Fragments are a special case, the function checks in the beginning if there are any Fragments specified in the
    GraphQL-Query. If not, the recursive function can be skipped and execution Performance gets improved.

    Parameters
    ----------
        selections: tuple
        fragment_selections: dict

    Returns
    -------
        tuple
    """
    # Check if there is no Fragment specified in the GraphQL-Query
    if not fragment_selections:
        return selections

    # Replace all the Fragments with the according Fields
    selections_list = []
    for selection in selections:
        if selection.kind == 'fragment_spread':
            if include_fragment(selection, variables):
                selections_list.extend(list(fragment_selections[selection.name.value]))
        else:
            # If there is a Child-Component call the Function Recursively
            if selection.selection_set is not None:
                selection.selection_set.selections = inject_graqhql_fragments(
                    selection.selection_set.selections, fragment_selections, variables)

            selections_list.append(selection)

    return tuple(selections_list)


def include_fragment(spread_node: FragmentSpreadNode, variables: dict) -> bool:
    """
    Takes a Fragment Spread Node and determines whether the Fragment gets applied or not based on additionally specified
    Directives. Since Directives are special cases the function checks in the beginning if a Directive specified to
    improve performance for the majority of Queries.

    Parameters
    ----------
        spread_node: FragmentSpreadNode
        variables: dict

    Returns
    -------
        bool
    """
    if len(spread_node.directives) == 0:
        return True

    directive_node: DirectiveNode = spread_node.directives[0]
    # Extracts either 'include' or 'skip'
    directive_type = directive_node.name.value
    # Replace Variable with Value if condition is defined in Variable
    if directive_node.arguments[0].value.kind == 'variable':
        directive_value = variables[directive_node.arguments[0].value.name.value]
    else:
        directive_value = directive_node.arguments[0].value.value

    # Decide if Fragment should be included or not
    if directive_type == 'include':
        return directive_value
    elif directive_type == 'skip':
        return not directive_value
    else:
        raise Exception(f"Unknown directive: {directive_type}")


def inject_graphql_variables(selections: tuple, variables: dict):
    """
    Takes the selections and Variables specified by the clients GraphQL-Query. The function works in a recursive
    approach through all objects, sub-objects, sub-sub-objects, ... in the query. For each object that contains
    arguments the inject_argument_variable gets called which replaces the actual Field with the Variable.
    Since Variables are a special case, the function checks in the beginning if there are any Variables specified in the
    GraphQL-Query. If not, the recursive function can be skipped and execution Performance gets improved.

    Parameters
    ----------
        selections: tuple
        variables: dict

    Returns
    -------
        tuple
    """
    # Check if there are no Variables specified in the GraphQL-Query
    if not variables:
        return selections

    # Loop through Fields
    for selection in selections:
        for argument in selection.arguments:
            # Replace Variables in Argument
            inject_argument_variable(argument.value, variables)

        # If there is a Child-Component call the Function Recursively on the Child-Content
        if selection.selection_set is not None:
            inject_graphql_variables(selection.selection_set.selections, variables)

    return selections


def inject_argument_variable(value_node, variables):
    """
        Takes one Argument and works recursively through the List / Object until it reaches the actual Field. If the
        actual Value is a Variable, it gets replaced by its actual Value.

        Parameters
        ----------
            value_node: ObjectNode | ListNode | FieldNode
            variables: dict
    """
    # If ObjectNode call function again with the Nodes of the Fields in the Object
    if value_node.kind == 'object_value':
        for field in value_node.fields:
            inject_argument_variable(field, variables)
    # If ListNode call function again for all Objects Nodes inside the List
    elif value_node.kind == 'list_value':
        for node in value_node.values:
            inject_argument_variable(node, variables)
    # If the Value Node contains an actual Variable, insert the Value for the Variable into the Datastructure
    elif value_node.kind == 'variable':
        value_node.value = VariableNode()
        setattr(value_node.value, 'value', variables[value_node.name.value])
    else:
        # If Field Node check what is behind the Field
        # If an Object Node is behind the Field call function again for all Nodes of the fields in the Object
        if value_node.value.kind == 'object_value':
            for field in value_node.value.fields:
                inject_argument_variable(field, variables)
        # If a List Node is behind the Field call function again for all Object Nodes inside the List
        elif value_node.value.kind == 'list_value':
            for node in value_node.value.values:
                inject_argument_variable(node, variables)
        # If the Value Node contains an actual Variable, insert the Value for the Variable into the Datastructure
        elif value_node.value.kind == 'variable':
            setattr(value_node.value, 'value', variables[value_node.value.name.value])
