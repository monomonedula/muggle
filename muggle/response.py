from abc import ABC, abstractmethod

from muggle.body import Body
from muggle.headofrequest import HeadOfResponse


class Response(HeadOfResponse, Body, ABC):
    @abstractmethod
    def status(self) -> str:
        pass
