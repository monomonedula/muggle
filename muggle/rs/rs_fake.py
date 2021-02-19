from typing import AsyncIterator, Optional

from multidict import MultiMapping, CIMultiDict, CIMultiDictProxy

from muggle.response import Response


class RsFake(Response):
    def __init__(
        self,
        status: str,
        headers: MultiMapping[str] = CIMultiDictProxy(CIMultiDict()),
        body: Optional[bytes] = None,
    ):
        self._status: status = status
        self._headers: MultiMapping[str] = headers
        self._body: bytes = body

    async def status(self) -> str:
        return self._status

    async def headers(self) -> MultiMapping[str]:
        return self._headers

    def body(self) -> AsyncIterator[bytes]:
        if self._body is not None:
            yield self._body
