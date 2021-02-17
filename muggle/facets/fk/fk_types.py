from itertools import chain
from typing import Optional, Union, Collection

from multidict import MultiMapping
from werkzeug.datastructures import MIMEAccept
from werkzeug.http import parse_accept_header

from muggle.fork import Fork
from muggle.mg.mg_fixed import MgFixed
from muggle.muggle import Muggle
from muggle.request import Request
from muggle.response import Response
from muggle.rs.rs_text import RsText


class FkTypes(Fork):
    def __init__(self, types: Collection[str], resp: Union[Muggle, Response, str]):
        self._types: Collection[str] = types
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
        headers: MultiMapping[str, str] = await request.headers()
        if MIMEAccept(
            chain.from_iterable(
                parse_accept_header(val, MIMEAccept)
                for val in headers.getall("Accept", ["text/html"])
            )
        ).best_match(self._types):
            return await self._mg.act(request)
