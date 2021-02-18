from collections import Collection

from multidict import MultiMapping, MultiDict

from muggle.request import Request
from muggle.rq.rq_wrap import RqWrap


class RqWithoutHeaders(RqWrap):
    def __init__(self, rq: Request, removed_headers: Collection[str]):
        self._rq: Request = rq
        self._headers: Collection[str] = removed_headers
        super(RqWithoutHeaders, self).__init__(rq)

    async def headers(self) -> MultiMapping[str, str]:
        headers: MultiMapping[str, str] = await self._rq.headers()
        new_headers: MultiDict[str, str] = MultiDict(headers)
        for h in self._headers:
            if h in new_headers:
                del new_headers[h]
        return new_headers
