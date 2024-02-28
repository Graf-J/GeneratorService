from typing import List

from querybuilder.arguments.logicunit import LogicUnit


class Logic:
    def __init__(self):
        self.EQ: None | LogicUnit = None
        self.NEQ: None | LogicUnit = None
        self.GT: None | LogicUnit = None
        self.GTE: None | LogicUnit = None
        self.LT: None | LogicUnit = None
        self.LTE: None | LogicUnit = None

        self.AND: None | List[Logic] = None
        self.OR: None | List[Logic] = None
