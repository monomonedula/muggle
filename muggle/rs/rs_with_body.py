from typing import AsyncIterator, Optional

from muggle.body import Body
from muggle.response import Response
from muggle.rs.rs_with_status import RsWithStatus
from muggle.rs.rs_wrap import RsWrap


class RsWithBody(RsWrap):
    def __init__(self, body: Body, response: Optional[Response] = None):
        self._body: Body = body
        super(RsWithBody, self).__init__(
            RsWithStatus(200) if response is None else response
        )

    def body(self) -> AsyncIterator[bytes]:
        return self._body.body()
