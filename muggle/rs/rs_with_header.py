from typing import Dict

from multidict import MultiMapping, CIMultiDict, CIMultiDictProxy

from muggle.response import Response
from muggle.rs.rs_wrap import RsWrap


class RsWithHeaders(RsWrap):
    def __init__(self, resp: Response, headers: Dict[str, str]):
        self._response: Response = resp
        self._headers: Dict[str, str] = headers
        super(RsWithHeaders, self).__init__(resp)

    async def headers(self) -> MultiMapping[str, str]:
        headers: MultiMapping[str, str] = await self._response.headers()
        new_headers: CIMultiDict[str, str] = CIMultiDict(headers)
        for h, v in self._headers.items():
            new_headers.add(h, v)
        return CIMultiDictProxy(new_headers)
