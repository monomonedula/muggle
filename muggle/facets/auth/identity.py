from abc import ABC, abstractmethod
from collections import Mapping
from types import MappingProxyType


class Identity(ABC):
    @abstractmethod
    async def urn(self) -> str:
        pass

    @abstractmethod
    async def properties(self) -> Mapping[str, str]:
        pass


class _Anonymous(Identity):
    async def urn(self) -> str:
        return NotImplementedError

    async def properties(self) -> Mapping[str, str]:
        raise NotImplementedError

    def __str__(self):
        return self.__class__.__name__


ANONYMOUS = _Anonymous()


class IdentitySimple(Identity):
    def __init__(self, urn: str, props: Mapping[str, str] = None):
        self._name: str = urn
        self._props: Mapping[str, str] = props if props is not None else MappingProxyType({})

    async def urn(self) -> str:
        return self._name

    async def properties(self) -> Mapping[str, str]:
        return self._props
