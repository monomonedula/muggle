from typing import Dict

from abc_delegation import delegation_metaclass

from muggle.response import Response


class RsWithHeaders(Response, metaclass=delegation_metaclass("_response")):
    def __init__(self, resp: Response, headers: Dict[str, str]):
        self._response: Response = resp
        self._headers: Dict[str, str] = headers

    async def headers(self) -> Dict[str, str]:
        headers: Dict[str, str] = await self._response.headers()
        for h, v in self._headers.items():
            headers[h] = v
        return headers
