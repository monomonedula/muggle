from typing import Optional

from muggle.fork import Fork
from muggle.muggle import Muggle
from muggle.request import Request
from muggle.response import Response


class FkFixed(Fork):
    def __init__(self, mg: Muggle):
        self._mg: Muggle = mg

    async def route(self, request: Request) -> Optional[Response]:
        return await self._mg.act(request)
