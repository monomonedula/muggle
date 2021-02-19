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


class FkContentType(Fork):
    def __init__(self, types: Collection[str], resp: Union[Response, Muggle]):
        self._mg: Muggle = MgFixed(resp) if isinstance(resp, Response) else resp
        self._ctypes: Collection[str] = types

    async def route(self, request: Request) -> Optional[Response]:
        headers: MultiMapping[str] = await request.headers()
        if MIMEAccept(
            chain.from_iterable(
                parse_accept_header(val, MIMEAccept)
                for val in headers.getall("Content-Type", ["*/*"])
            )
        ).best_match(self._ctypes):
            return await self._mg.act(request)
        return None
