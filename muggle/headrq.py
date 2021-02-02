from abc import ABC, abstractmethod
from typing import Dict

from muggle.primitives.scalar import Scalar, scalar


class HeadRs(ABC):
    @abstractmethod
    def headers(self) -> Scalar[Dict[str, str]]:
        pass


class HeadRq(ABC):
    @abstractmethod
    def headers(self) -> Scalar[Dict[str, str]]:
        pass

    @abstractmethod
    def uri(self) -> Scalar[str]:
        pass

    @abstractmethod
    def method(self) -> Scalar[str]:
        pass


class SimpleHeadRq(HeadRq):
    def __init__(self, headers: Dict[str, str], uri="/", method="GET"):
        self._headers: Dict[str, str] = headers
        self._uri: str = uri
        self._method: str = method

    def headers(self) -> Scalar[Dict[str, str]]:
        return scalar(self._headers.copy())

    def uri(self) -> Scalar[str]:
        return scalar(self._uri)

    def method(self) -> Scalar[str]:
        return scalar(self._method)
