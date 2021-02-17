from typing import Optional

from muggle.fork import Fork
from muggle.muggle import Muggle
from muggle.request import Request
from muggle.response import Response


class FkHost(Fork):
    def __init__(self, host: str, mg: Muggle):
        self._host: str = host
        self._mg: Muggle = mg

    async def route(self, request: Request) -> Optional[Response]:
        if (await request.headers())["host"] == self._host:
            return await self._mg.act(request)

