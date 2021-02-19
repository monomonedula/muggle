from typing import AsyncIterator

from multidict import MultiMapping

from muggle.response import Response


class RsWrap(Response):
    def __init__(self, rs: Response):
        self.__origin: Response = rs

    async def status(self) -> str:
        return await self.__origin.status()

    async def headers(self) -> MultiMapping[str]:
        return await self.__origin.headers()

    def body(self) -> AsyncIterator[bytes]:
        return self.__origin.body()
