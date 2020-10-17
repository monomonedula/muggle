import re
from typing import Union, Pattern, Optional, AsyncGenerator, Dict

from muggle.fork import Fork
from muggle.http_exception import HttpException
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

    async def route(self, request: Request) -> Optional[Response]:
        if self._pattern.match(await request.uri()):
            return self._mg.act(request)


class ResponseForked(Response):
    def __init__(self, fork: Fork, request: Request):
        self._fork = fork
        self._rq = request
        self._resp = None

    async def status(self) -> str:
        return await (await self._response()).status()

    async def headers(self) -> Dict[str, str]:
        return await (await self._response()).headers()

    async def body(self) -> AsyncGenerator[bytes]:
        return await (await self._response()).body()

    async def _response(self) -> Response:
        if self._resp is None:
            resp = await self._fork.route(self._rq)
            if resp is None:
                raise HttpException(404)
            self._resp = resp
        return self._resp
