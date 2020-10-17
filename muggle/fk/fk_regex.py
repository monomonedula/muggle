import re
from typing import Union, Pattern, Optional, AsyncGenerator, Dict

from muggle.fork import Fork
from muggle.mg.mg_fixed import MgFixed
from muggle.muggle import Muggle
from muggle.request import Request
from muggle.response import Response
from muggle.rs.rs_text import RsText


class FkRegex(Fork):
    def __init__(
        self, pattern: Union[str, Pattern], *, resp: Union[Muggle, Response, str]
    ):
        self._pattern = (
            pattern if isinstance(pattern, re.Pattern) else re.compile(pattern)
        )
        if isinstance(resp, str):
            self._mg = MgFixed(RsText(resp))
        elif isinstance(resp, Response):
            self._mg = MgFixed(resp)
        elif isinstance(resp, Muggle):
            self._mg = resp
        else:
            raise TypeError("Expected Response, Muggle or str. Got: %r" % type(resp))

    def route(self, request: Request) -> Optional[Response]:
        if self._pattern.match(request.uri()):
            return self._mg.act(request)


class ResponseForked(Response):
    def __init__(self, resp):
        self._foo = fork

    async def status(self) -> str:
        pass

    async def headers(self) -> Dict[str, str]:
        pass

    async def body(self) -> AsyncGenerator[bytes]:
        pass
