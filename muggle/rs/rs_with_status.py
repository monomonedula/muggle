from http import HTTPStatus

from muggle.response import Response
from muggle.rs.rs_empty import RsEmpty
from muggle.rs.rs_wrap import RsWrap


class RsWithStatus(RsWrap):
    _codes = {code.value: code.phrase for code in HTTPStatus}

    def __init__(self, status, reason: str = None, response: Response = None):
        if status < 100 or status > 999:
            raise TypeError("Bad status code: %r" % status)
        self._status = status
        self._reason = reason or self._codes[status]
        super(RsWithStatus, self).__init__(RsEmpty() if response is None else response)

    async def status(self) -> str:
        return f"{self._status} {self._reason}"
