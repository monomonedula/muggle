from typing import AsyncIterator, Optional

from abc_delegation import delegation_metaclass

from muggle.body import Body
from muggle.response import Response
from muggle.rs.rs_with_status import RsWithStatus


class RsWithBody(Response, metaclass=delegation_metaclass("_response")):
    def __init__(self, body: Body, response: Optional[Response] = None):
        if response is None:
            response = RsWithStatus(200)
        self._response: Response = response
        self._body: Body = body

    def body(self) -> AsyncIterator[bytes]:
        return self._body.body()
