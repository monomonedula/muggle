from typing import Dict, AsyncGenerator

from muggle.response import Response


class RsEmpty(Response):
    async def status(self) -> str:
        return "204 No Content"

    async def headers(self) -> Dict[str, str]:
        return {}

    async def body(self) -> AsyncGenerator[bytes]:
        return
        # noinspection PyUnreachableCode
        yield
