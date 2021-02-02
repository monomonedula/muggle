from typing import Optional

from abc_delegation import delegation_metaclass

from muggle.response import Response
from muggle.rs.rs_with_header import RsWithHeaders


class RsWithType(Response, metaclass=delegation_metaclass("_response")):
    def __init__(self, response: Response, type_: str, charset: Optional[str] = None):
        if charset is None:
            response = RsWithHeaders(response, {"Content-Type": type_})
        else:
            response = RsWithHeaders(
                response, {"Content-Type": f"{type_}; charset={charset}"}
            )
        self._response: Response = response
