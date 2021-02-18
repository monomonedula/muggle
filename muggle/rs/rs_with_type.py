from typing import Optional

from muggle.response import Response
from muggle.rs.rs_with_header import RsWithHeaders
from muggle.rs.rs_wrap import RsWrap


class RsWithType(RsWrap):
    def __init__(self, response: Response, type_: str, charset: Optional[str] = None):
        super(RsWithType, self).__init__(
            RsWithHeaders(response, {"Content-Type": type_})
            if charset is None
            else RsWithHeaders(
                response, {"Content-Type": f"{type_}; charset={charset}"}
            )
        )
