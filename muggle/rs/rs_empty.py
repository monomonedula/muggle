from typing import AsyncIterator

from multidict import MultiMapping, MultiDict

from muggle.response import Response


class RsEmpty(Response):
    async def status(self) -> str:
        return "204 No Content"

    async def headers(self) -> MultiMapping[str]:
        return MultiDict()

    async def body(self) -> AsyncIterator[bytes]:
        return
        # noinspection PyUnreachableCode
        yield b""
