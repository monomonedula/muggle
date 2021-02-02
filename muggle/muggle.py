from abc import ABC, abstractmethod

from muggle.request import Request
from muggle.response import Response


class Muggle(ABC):
    @abstractmethod
    async def act(self, request: Request) -> Response:
        pass
