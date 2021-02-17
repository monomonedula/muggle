from typing import Collection

from abc_delegation import delegation_metaclass
from multidict import MultiMapping, MultiDict

from muggle.response import Response


class RsWithoutHeaders(Response, metaclass=delegation_metaclass("_response")):
    def __init__(self, resp: Response, removed_headers: Collection[str]):
        self._response = resp
        self._headers: Collection[str] = removed_headers

    async def headers(self) -> MultiMapping[str, str]:
        headers: MultiMapping[str, str] = await self._response.headers()
        new_headers: MultiDict[str, str] = MultiDict(headers)
        for h in self._headers:
            del new_headers[h]
        return new_headers
