from typing import Optional

from muggle.facets.auth.codecs.codec_plain import CcPlain
from muggle.facets.auth.identity import Identity, ANONYMOUS
from muggle.facets.auth.mg_auth import MgAuth
from muggle.request import Request
from muggle.rq.rq_wrap import RqWrap


class RqAuth(RqWrap):
    def __init__(self, rq: Request, header: str = MgAuth.__class__.__name__):
        self._header: str = header
        super(RqAuth, self).__init__(rq)

    async def identity(self) -> Identity:
        header_value: Optional[str] = (await self.headers()).getone(self._header, None)
        user: Identity
        if header_value is None:
            user = ANONYMOUS
        else:
            user = await CcPlain().decode(header_value)
        return user
