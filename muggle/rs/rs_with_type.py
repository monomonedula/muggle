from typing import Dict, BinaryIO

from abc_delegation import delegation_metaclass

from muggle.response import Response
from muggle.rs.rs_with_header import RsWithHeader


class RsWithType(Response, metaclass=delegation_metaclass("_response")):
    def __init__(self, response: Response, type_: str, charset=None):
        if charset:
            response = RsWithHeader(response, "Content-Type", type_)
        else:
            response = RsWithHeader(
                response, "Content-Type", f"{type_}; charset={charset}"
            )
        self._response = response
