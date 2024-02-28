from collections import deque
from typing import TypeVar, Generic

T = TypeVar('T')


class Stack(Generic[T]):
    def __init__(self):
        self.deq = deque()

    def push(self, item: T):
        self.deq.append(item)

    def pop(self) -> T:
        return self.deq.pop()

    def peek(self) -> T:
        return self.deq[-1]
