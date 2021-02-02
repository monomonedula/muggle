import re
from typing import Union, Pattern, Optional, Dict, AsyncIterator

from muggle.fork import Fork
from muggle.mg.mg_fixed import MgFixed
from muggle.muggle import Muggle
from muggle.request import Request
from muggle.response import Response
from muggle.rs.rs_text import RsText
from muggle.rs.rs_with_status import RsWithStatus


class FkRegex(Fork):
    def __init__(
        self, pattern: Union[str, Pattern], *, resp: Union[Muggle, Response, str]
    ):
        self._pattern = (
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
        if self._pattern.match(await request.uri()):
            return await self._mg.act(request)


class ResponseForked(Response):
    def __init__(
        self,
        fork: Fork,
        request: Request,
        fallback_response: Response = RsWithStatus(404),
    ):
        self._fork: Fork = fork
        self._rq: Request = request
        self._fb: Response = fallback_response
        self._resp: Optional[Response] = None

    async def status(self) -> str:
        resp = await self._response()
        return await resp.status()

    async def headers(self) -> Dict[str, str]:
        resp = await self._response()
        return await resp.headers()

    async def body(self) -> AsyncIterator[bytes]:
        async for chunk in (await self._response()).body():
            yield chunk

    async def _response(self) -> Response:
        if self._resp is None:
            self._resp = await self._fork.route(self._rq) or self._fb
        return self._resp
