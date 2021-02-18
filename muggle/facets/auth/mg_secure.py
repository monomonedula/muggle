from muggle.facets.auth.identity import ANONYMOUS
from muggle.facets.auth.rq_auth import RqAuth
from muggle.http_exception import HttpException
from muggle.muggle import Muggle
from muggle.request import Request
from muggle.response import Response


class MgSecure(Muggle):
    def __init__(self, mg: Muggle):
        self._origin: Muggle = mg

    async def act(self, request: Request) -> Response:
        if await RqAuth(request).identity() is ANONYMOUS:
            raise HttpException(303)
        return await self._origin.act(request)
