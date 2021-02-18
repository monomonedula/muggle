from abc import ABC, abstractmethod
from typing import Optional

from muggle.facets.auth.identity import Identity
from muggle.request import Request
from muggle.response import Response


class Pass(ABC):
    @abstractmethod
    async def enter(self, request: Request) -> Optional[Identity]:
        pass

    @abstractmethod
    async def exit(self, response: Response) -> Response:
        pass
