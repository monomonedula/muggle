from typing import Dict

from abc_delegation import delegation_metaclass
from multidict import MultiMapping, MultiDict

from muggle.response import Response


class RsWithHeaders(Response, metaclass=delegation_metaclass("_response")):
    def __init__(self, resp: Response, headers: Dict[str, str]):
        self._response: Response = resp
        self._headers: Dict[str, str] = headers

    async def headers(self) -> MultiMapping[str, str]:
        headers: MultiMapping[str, str] = await self._response.headers()
        new_headers: MultiDict[str, str] = MultiDict(headers)
        for h, v in self._headers.items():
            new_headers.add(h, v)
        return new_headers
