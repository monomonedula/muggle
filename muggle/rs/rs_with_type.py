from typing import Optional

from muggle.response import Response
from muggle.rs.rs_with_header import RsWithHeaders
from muggle.rs.rs_without_header import RsWithoutHeaders
from muggle.rs.rs_wrap import RsWrap


class RsWithType(RsWrap):
    def __init__(self, response: Response, type_: str, charset: Optional[str] = None):
        response = RsWithoutHeaders(response, ["Content-Type"])
        super(RsWithType, self).__init__(
            RsWithHeaders(response, {"Content-Type": type_})
            if charset is None
            else RsWithHeaders(
                response, {"Content-Type": f"{type_}; charset={charset}"}
            )
        )


class Json(RsWrap):
    def __init__(self, response: Response, charset: Optional[str] = None):
        super(Json, self).__init__(RsWithType(response, "application/json", charset))


class Xml(RsWrap):
    def __init__(self, response: Response, charset: Optional[str] = None):
        super(Xml, self).__init__(RsWithType(response, "text/xml", charset))


class Html(RsWrap):
    def __init__(self, response: Response, charset: Optional[str] = None):
        super(Html, self).__init__(RsWithType(response, "text/html", charset))


class Text(RsWrap):
    def __init__(self, response: Response, charset: Optional[str] = None):
        super(Text, self).__init__(RsWithType(response, "text/plain", charset))
