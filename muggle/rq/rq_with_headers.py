from typing import Dict

from multidict import MultiMapping, MultiDict

from muggle.request import Request
from muggle.rq.rq_wrap import RqWrap


class RqWithHeaders(RqWrap):
    def __init__(self, rq: Request, headers: Dict[str, str]):
        self._rq: RqWithHeaders = rq
        self._headers: Dict[str, str] = headers
        super(RqWithHeaders, self).__init__(rq)

    async def headers(self) -> MultiMapping[str, str]:
        headers: MultiMapping[str, str] = await self._rq.headers()
        new_headers: MultiDict[str, str] = MultiDict(headers)
        for h, v in self._headers.items():
            new_headers.add(h, v)
        return new_headers
