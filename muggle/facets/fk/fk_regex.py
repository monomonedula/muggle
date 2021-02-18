import re
from typing import Union, Pattern, Optional, Dict, AsyncIterator

from multidict import MultiMapping

from muggle.fork import Fork
from muggle.mg.mg_fixed import MgFixed
from muggle.muggle import Muggle
from muggle.request import Request
from muggle.response import Response
from muggle.rs.rs_text import RsText
from muggle.rs.rs_with_status import RsWithStatus


class FkRegex(Fork):
    """
    Fork by regular expression pattern.

    This class is immutable and coroutine-safe.
    """

    def __init__(
        self, pattern: Union[str, Pattern], *, resp: Union[Muggle, Response, str]
    ):
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
        if self._pattern.match((await request.uri()).path):
            return await self._mg.act(request)
