from typing import Dict

from multidict import MultiMapping, CIMultiDict, CIMultiDictProxy

from muggle.request import Request
from muggle.rq.rq_wrap import RqWrap


class RqWithHeaders(RqWrap):
    def __init__(self, rq: Request, headers: Dict[str, str]):
        self._rq: Request = rq
        self._headers: Dict[str, str] = headers
        super(RqWithHeaders, self).__init__(rq)

    async def headers(self) -> MultiMapping[str]:
        headers: MultiMapping[str] = await self._rq.headers()
        new_headers: CIMultiDict[str] = CIMultiDict(headers)
        for h, v in self._headers.items():
            new_headers.add(h, v)
        return CIMultiDictProxy(new_headers)
