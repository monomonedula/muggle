from typing import Collection

from multidict import MultiMapping, MultiDict

from muggle.response import Response
from muggle.rs.rs_wrap import RsWrap


class RsWithoutHeaders(RsWrap):
    def __init__(self, resp: Response, removed_headers: Collection[str]):
        self._response = resp
        self._headers: Collection[str] = removed_headers
        super(RsWithoutHeaders, self).__init__(resp)

    async def headers(self) -> MultiMapping[str, str]:
        headers: MultiMapping[str, str] = await self._response.headers()
        new_headers: MultiDict[str, str] = MultiDict(headers)
        for h in self._headers:
            del new_headers[h]
        return new_headers
