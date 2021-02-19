from collections import Collection

from multidict import MultiMapping, CIMultiDict, CIMultiDictProxy

from muggle.request import Request
from muggle.rq.rq_wrap import RqWrap


class RqWithoutHeaders(RqWrap):
    def __init__(self, rq: Request, removed_headers: Collection[str]):
        self._rq: Request = rq
        self._headers: Collection[str] = removed_headers
        super(RqWithoutHeaders, self).__init__(rq)

    async def headers(self) -> MultiMapping[str]:
        headers: MultiMapping[str] = await self._rq.headers()
        new_headers: CIMultiDict[str] = CIMultiDict(headers)
        for h in self._headers:
            if h in new_headers:
                del new_headers[h]
        return CIMultiDictProxy(new_headers)
