from querybuilder.arguments.orderdirection import OrderDirection


class Order:
    def __init__(self, prop: str, order: OrderDirection):
        self.property = prop
        self.order = order
