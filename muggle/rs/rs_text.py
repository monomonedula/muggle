from typing import Union, TextIO, Optional

from muggle.body import TextBody
from muggle.response import Response
from muggle.rs.rs_with_body import RsWithBody
from muggle.rs.rs_with_status import RsWithStatus
from muggle.rs.rs_with_type import RsWithType
from muggle.rs.rs_wrap import RsWrap


class RsText(RsWrap):
    def __init__(
        self, text: Union[str, bytes, TextIO] = "", response: Optional[Response] = None
    ):
        response: Response
        if response is None:
            response = RsWithStatus(200)
        if text:
            response = RsWithBody(TextBody(text), response)
        super(RsText, self).__init__(RsWithType(response, "text/plain"))
