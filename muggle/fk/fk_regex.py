import re
from typing import Union, Pattern, Optional, Dict, AsyncIterator, TypeVar, Awaitable, Callable

from muggle.fork import Fork
from muggle.mg.mg_fixed import MgFixed
from muggle.muggle import Muggle
from muggle.primitives.scalar import Scalar
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
        if isinstance(resp, str):
            self._mg = MgFixed(RsText(resp))
        elif isinstance(resp, Response):
            self._mg = MgFixed(resp)
        elif isinstance(resp, Muggle):
            self._mg = resp
        else:
            raise TypeError("Expected Response, Muggle or str. Got: %r" % type(resp))

    async def route(self, request: Request) -> Optional[Response]:
        if self._pattern.match(await request.uri().value()):
            return self._mg.act(request)


class ResponseForked(Response):
    def __init__(self, fork: Fork, request: Request, fallback_response=RsWithStatus(404)):
        self._fork = fork
        self._rq = request
        self._fb = fallback_response
        self._resp = None

    def status(self) -> Scalar[str]:
        return ScalarOfCoro(
            lambda: _call_method(self._response, "status")
        )

    def headers(self) -> Scalar[Dict[str, str]]:
        return ScalarOfCoro(
            lambda: _call_method(self._response, "headers")
        )

    async def body(self) -> AsyncIterator[bytes]:
        async for chunk in (await self._response()).body():
            yield chunk

    async def _response(self) -> Response:
        if self._resp is None:
            self._resp = await self._fork.route(self._rq) or self._fb
        return self._resp


async def _call_method(get_obj: Callable[[], Awaitable[Response]], method_name: str):
    return getattr((await get_obj()), method_name)()


T = TypeVar('T')


class ScalarOfCoro(Scalar[T]):
    def __init__(self, get_value: Callable[[], Awaitable[T]]):
        self.__value: Callable[[], Awaitable[T]] = get_value

    async def value(self) -> T:
        return await self.__value()
