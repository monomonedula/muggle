from typing import Dict, Collection

from abc_delegation import delegation_metaclass

from muggle.response import Response


class RsWithoutHeaders(Response, metaclass=delegation_metaclass("_response")):
    def __init__(self, resp: Response, removed_headers: Collection[str]):
        self._response = resp
        self._headers: Collection[str] = removed_headers

    async def headers(self) -> Dict[str, str]:
        headers: Dict[str, str] = await self._response.headers()
        for h in self._headers:
            del headers[h]
        return headers
