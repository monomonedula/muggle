from http import HTTPStatus

from abc_delegation import delegation_metaclass

from muggle.response import Response
from muggle.rs.rs_empty import RsEmpty


class RsWithStatus(Response, metaclass=delegation_metaclass("_response")):
    _codes = {code.value: code.phrase for code in HTTPStatus}

    def __init__(self, status, reason: str = None, response: Response = None):
        if status < 100 or status > 999:
            raise TypeError("Bad status code: %r" % status)
        self._status = status
        self._reason = reason or self._codes[status]
        self._response = response or RsEmpty()

    async def status(self) -> str:
        return f"{self._status} {self._reason}"
