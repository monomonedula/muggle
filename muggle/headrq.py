from abc import ABC, abstractmethod
from urllib.parse import ParseResult, urlparse

from multidict import MultiMapping


class HeadRs(ABC):
    @abstractmethod
    async def headers(self) -> MultiMapping[str, str]:
        pass


class HeadRq(ABC):
    @abstractmethod
    async def headers(self) -> MultiMapping[str, str]:
        pass

    @abstractmethod
    async def uri(self) -> ParseResult:
        pass

    @abstractmethod
    async def method(self) -> str:
        pass


class SimpleHeadRq(HeadRq):
    def __init__(self, headers: MultiMapping[str, str], uri="/", method="GET"):
        self._headers: MultiMapping[str, str] = headers
        self._uri: str = uri
        self._method: str = method

    async def headers(self) -> MultiMapping[str, str]:
        return self._headers

    async def uri(self) -> ParseResult:
        return urlparse(self._uri)

    async def method(self) -> str:
        return self._method
