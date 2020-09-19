from abc import ABC, abstractmethod
from typing import Dict


class HeadOfResponse(ABC):
    @abstractmethod
    def headers(self) -> Dict[str, str]:
        pass


class HeadOfRequest(ABC):
    @abstractmethod
    def headers(self) -> Dict[str, str]:
        pass

    @abstractmethod
    def uri(self) -> str:
        pass

    @abstractmethod
    def method(self) -> str:
        pass


class SimpleHeadOfRequest(HeadOfRequest):
    def __init__(self, headers: Dict[str, str], uri="/", method="GET"):
        self._headers = headers
        self._uri = uri
        self._method = method

    def headers(self) -> Dict[str, str]:
        return self._headers.copy()

    def uri(self) -> str:
        return self._uri

    def method(self) -> str:
        return self._method
