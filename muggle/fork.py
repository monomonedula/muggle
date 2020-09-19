from abc import ABC, abstractmethod
from typing import Optional

from muggle.request import Request
from muggle.response import Response


class Fork(ABC):
    @abstractmethod
    def route(self, request: Request) -> Optional[Response]:
        pass
