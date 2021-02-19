from typing import Collection


from multidict import MultiMapping, CIMultiDict, CIMultiDictProxy

from muggle.response import Response
from muggle.rs.rs_wrap import RsWrap


class RsWithoutHeaders(RsWrap):
    def __init__(self, resp: Response, removed_headers: Collection[str]):
        self._response = resp
        self._headers: Collection[str] = removed_headers
        super(RsWithoutHeaders, self).__init__(resp)

    async def headers(self) -> MultiMapping[str]:
        headers: MultiMapping[str] = await self._response.headers()
        new_headers: CIMultiDict[str] = CIMultiDict(headers)
        for h in self._headers:
            if h in new_headers:
                del new_headers[h]
        return CIMultiDictProxy(new_headers)
