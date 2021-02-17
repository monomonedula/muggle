import re
from typing import Optional, Union, Pattern
from urllib.parse import urlparse, parse_qsl

from muggle.fork import Fork
from muggle.mg.mg_fixed import MgFixed
from muggle.muggle import Muggle
from muggle.request import Request
from muggle.response import Response
from muggle.rs.rs_text import RsText


class FkParams(Fork):
    """
    Fork by query params and their values, matched by regular expression.

    This class is immutable and thread safe.
    """
    def __init__(self, param: str, pattern: Union[str, Pattern], resp: Union[Muggle, Response, str]):
        self._param: str = param
        self._pattern: Pattern = (
            pattern if isinstance(pattern, re.Pattern) else re.compile(pattern)
        )
        self._mg: Muggle
        if isinstance(resp, str):
            self._mg = MgFixed(RsText(resp))
        elif isinstance(resp, Response):
            self._mg = MgFixed(resp)
        elif isinstance(resp, Muggle):
            self._mg = resp
        else:
            raise TypeError("Expected Response, Muggle or str. Got: %r" % type(resp))

    async def route(self, request: Request) -> Optional[Response]:
        for param, value in parse_qsl((await request.uri()).query):
            if param == self._param and self._pattern.match(value):
                return await self._mg.act(request)
