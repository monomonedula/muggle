from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')


class Scalar(ABC, Generic[T]):
    @abstractmethod
    async def value(self) -> T:
        pass


class scalar(Scalar):
    def __init__(self, val: T):
        self.__val: T = val

    async def value(self) -> T:
        return self.__val


class scalar_copied(Scalar):
    def __init__(self, val: T):
        self.__val: T = val

    async def value(self) -> T:
        return self.__val.copy()
