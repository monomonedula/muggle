from typing import AsyncGenerator

from abc_delegation import delegation_metaclass

from muggle.body import Body
from muggle.response import Response
from muggle.rs.rs_with_status import RsWithStatus


class RsWithBody(Response, metaclass=delegation_metaclass("_response")):
    def __init__(self, body: Body, response: Response = None):
        if response is None:
            response = RsWithStatus(200)
        self._response = response
        self._body = body

    async def body(self) -> AsyncGenerator[bytes]:
        return await self._body.body()
