from typing import Dict

from abc_delegation import delegation_metaclass

from muggle.response import Response


class RsWithoutHeader(Response, metaclass=delegation_metaclass("_response")):
    def __init__(self, resp: Response, header: str):
        self._response = resp
        self._header = header

    def headers(self) -> Dict[str, str]:
        headers = self._response.headers()
        if self._header in headers:
            del headers[self._header]
        return headers
