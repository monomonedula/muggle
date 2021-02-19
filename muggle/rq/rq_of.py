from typing import AsyncIterator
from urllib.parse import ParseResult

from multidict import MultiMapping

from muggle.body import Body
from muggle.headrq import HeadRq
from muggle.request import Request


class RqOf(Request):
    def __init__(self, head: HeadRq, body: Body):
        self._body: Body = body
        self._head: HeadRq = head

    async def headers(self) -> MultiMapping[str]:
        return await self._head.headers()

    def body(self) -> AsyncIterator[bytes]:
        return self._body.body()

    async def uri(self) -> ParseResult:
        return await self._head.uri()

    async def method(self) -> str:
        return await self._head.method()
