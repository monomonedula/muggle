from typing import Union, TextIO, Optional

from abc_delegation import delegation_metaclass

from muggle.body import TextBody
from muggle.response import Response
from muggle.rs.rs_with_body import RsWithBody
from muggle.rs.rs_with_status import RsWithStatus
from muggle.rs.rs_with_type import RsWithType


class RsText(Response, metaclass=delegation_metaclass("_response")):
    def __init__(self, text: Union[str, bytes, TextIO] = "", response: Optional[Response] = None):
        response: Response
        if response is None:
            response = RsWithStatus(200)
        if text:
            response = RsWithBody(TextBody(text), response)
        self._response: Response = RsWithType(response, "text/plain")
