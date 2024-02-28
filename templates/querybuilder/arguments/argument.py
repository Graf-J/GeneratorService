from enum import Enum


class Argument(Enum):
    PAGINATION = 'pagination'
    VERTEX_ORDER = 'orderByVertex'
    EDGE_ORDER = 'orderByEdge'
    VERTEX_LOGIC = 'whereVertex'
    EDGE_LOGIC = 'whereEdge'
