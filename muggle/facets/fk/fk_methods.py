from typing import Optional, Tuple, Union

from muggle.fork import Fork
from muggle.mg.mg_fixed import MgFixed
from muggle.muggle import Muggle
from muggle.request import Request
from muggle.response import Response


class FkMethods(Fork):
    def __init__(self, *methods: str, resp: Union[Muggle, Response]):
        self._methods: Tuple[str, ...] = methods
        self._mg: Muggle
        if isinstance(resp, Response):
            self._mg = MgFixed(resp)
        elif isinstance(resp, Muggle):
            self._mg = resp
        else:
            raise TypeError("Expected Response, Muggle or str. Got: %r" % type(resp))

    async def route(self, request: Request) -> Optional[Response]:
        if await request.method() in self._methods:
            return await self._mg.act(request)
