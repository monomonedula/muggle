from typing import Dict

from abc_delegation import delegation_metaclass

from muggle.response import Response


class RsWithHeader(Response, metaclass=delegation_metaclass("_response")):
    def __init__(self, resp: Response, header: str, value: str):
        self._response = resp
        self._header = header
        self._value = value

    def headers(self) -> Dict[str, str]:
        headers = self._response.headers()
        headers[self._header] = self._value
        return headers
