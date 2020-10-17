from abc import ABC, abstractmethod
from typing import Dict


class HeadOfResponse(ABC):
    @abstractmethod
    async def headers(self) -> Dict[str, str]:
        pass


class HeadOfRequest(ABC):
    @abstractmethod
    async def headers(self) -> Dict[str, str]:
        pass

    @abstractmethod
    async def uri(self) -> str:
        pass

    @abstractmethod
    async def method(self) -> str:
        pass


class SimpleHeadOfRequest(HeadOfRequest):
    def __init__(self, headers: Dict[str, str], uri="/", method="GET"):
        self._headers = headers
        self._uri = uri
        self._method = method

    async def headers(self) -> Dict[str, str]:
        return self._headers.copy()

    async def uri(self) -> str:
        return self._uri

    async def method(self) -> str:
        return self._method
