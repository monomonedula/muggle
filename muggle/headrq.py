from abc import ABC, abstractmethod
from typing import Dict


class HeadRs(ABC):
    @abstractmethod
    async def headers(self) -> Dict[str, str]:
        pass


class HeadRq(ABC):
    @abstractmethod
    async def headers(self) -> Dict[str, str]:
        pass

    @abstractmethod
    async def uri(self) -> str:
        pass

    @abstractmethod
    async def method(self) -> str:
        pass


class SimpleHeadRq(HeadRq):
    def __init__(self, headers: Dict[str, str], uri="/", method="GET"):
        self._headers: Dict[str, str] = headers
        self._uri: str = uri
        self._method: str = method

    async def headers(self) -> Dict[str, str]:
        return self._headers.copy()

    async def uri(self) -> str:
        return self._uri

    async def method(self) -> str:
        return self._method
