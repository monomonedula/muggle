from typing import Dict, AsyncIterator

from muggle.primitives.scalar import Scalar, scalar
from muggle.response import Response


class RsEmpty(Response):
    def status(self) -> Scalar[str]:
        return scalar("204 No Content")

    def headers(self) -> Scalar[Dict[str, str]]:
        return scalar({})

    async def body(self) -> AsyncIterator[bytes]:
        return
        # noinspection PyUnreachableCode
        yield b""
