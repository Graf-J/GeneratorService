from abc import ABC, abstractmethod


class Mapper(ABC):
    @staticmethod
    @abstractmethod
    def to_dto(entity):
        pass

    @staticmethod
    @abstractmethod
    def to_entity(dto):
        pass
