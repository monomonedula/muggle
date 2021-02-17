from typing import Optional, Union

from multidict import MultiMapping

from muggle.facets.auth.codecs.codec_plain import CcPlain
from muggle.facets.auth.identity import Identity, IdentitySimple, ANONYMOUS
from muggle.muggle import Muggle
from muggle.request import Request
from muggle.response import Response
from muggle.facets.auth.pass_ import Pass
from muggle.rq.rq_with_headers import RqWithHeaders
from muggle.rq.rq_without_header import RqWithoutHeaders
from muggle.rq.rq_wrap import RqWrap


class MgAuth(Muggle):
    def __init__(self, mg: Muggle, pss: Pass, header: Optional[str] = None):
        self._mg: Muggle = mg
        self._pass: Pass = pss
        self._header: str = header or MgAuth.__class__.__name__

    async def act(self, request: Request) -> Response:
        user: Optional[Identity] = await self._pass.enter(request)
        response: Response
        if user is not None:
            response = await self.act_identified(request, user)
        else:
            response = await self._mg.act(request)
        return response

    async def act_identified(self, request: Request, identity: Identity) -> Response:
        return await self._pass.exit(
            self._mg.act(
                RqWithoutHeaders(request, [self._header])
                if identity is ANONYMOUS
                else RqWithAuth(
                    identity=identity,
                    header=self._header,
                    rq=RqWithoutHeaders(request, [self._header]),
                )
            )
        )


class RqWithAuth(RqWrap):
    def __init__(
        self,
        identity: Union[str, Identity],
        rq: Request,
        header: str = MgAuth.__class__.__name__,
    ):
        self._identity: Identity = (
            IdentitySimple(urn=identity) if isinstance(identity, str) else identity
        )
        self._rq: Request = rq
        self._header: str = header
        super(RqWithAuth, self).__init__(rq)

    async def headers(self) -> MultiMapping[str, str]:
        return await RqWithHeaders(
            self._rq, {self._header: (await CcPlain().encode(self._identity)).decode()}
        ).headers()
