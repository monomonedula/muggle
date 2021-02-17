from itertools import chain
from typing import Optional, Union, List

from werkzeug.http import parse_accept_header

from muggle.fork import Fork
from muggle.mg.mg_fixed import MgFixed
from muggle.muggle import Muggle
from muggle.request import Request
from muggle.response import Response


class FkEncoding(Fork):
    def __init__(self, encoding: str, resp: Union[Response, Muggle]):
        self._mg: Muggle = MgFixed(resp) if isinstance(resp, Response) else resp
        self._encoding: str = encoding

    async def route(self, request: Request) -> Optional[Response]:
        headers: Optional[List[str]] = (await request.headers()).getall("accept-encoding")
        response: Optional[Response] = None
        if not headers:
            response = await self._mg.act(request)
        elif self._encoding and self._encoding in [
            enc for enc, priority in
            chain.from_iterable(
                parse_accept_header(val)
                for val in headers
            )
        ]:
            response = await self._mg.act(request)
        return response

