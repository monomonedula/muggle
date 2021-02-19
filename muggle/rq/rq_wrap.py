from typing import AsyncIterator
from urllib.parse import ParseResult

from multidict import MultiMapping

from muggle.request import Request


class RqWrap(Request):
    def __init__(self, rq: Request):
        self.__origin = rq

    async def headers(self) -> MultiMapping[str]:
        return await self.__origin.headers()

    async def uri(self) -> ParseResult:
        return await self.__origin.uri()

    async def method(self) -> str:
        return await self.__origin.method()

    def body(self) -> AsyncIterator[bytes]:
        return self.__origin.body()
