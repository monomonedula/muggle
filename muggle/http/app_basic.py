from multidict import CIMultiDict, CIMultiDictProxy

from muggle.body import BodyFromASGI
from muggle.headrq import SimpleHeadRq
from muggle.http_exception import HttpException
from muggle.muggle import Muggle
from muggle.response import Response
from muggle.rq.rq_of import RqOf
from muggle.rs.rs_with_status import RsWithStatus


class AppBasic:
    def __init__(self, muggle: Muggle):
        self._muggle: Muggle = muggle

    async def __call__(self, scope, receive, send):
        try:
            await _respond(
                await self._muggle.act(
                    RqOf(
                        SimpleHeadRq(
                            CIMultiDictProxy(CIMultiDict(scope["headers"])), scope["path"], scope["method"]
                        ),
                        BodyFromASGI(receive),
                    )
                ),
                send,
            )
        except HttpException as e:
            await _respond(RsWithStatus(e.code()), send)


async def _respond(response: Response, send):
    await send(
        {
            "type": "http.response.start",
            "status": await response.status(),
            "headers": await response.headers(),
        }
    )
    async for body_chunk in response.body():
        await send(
            {
                "type": "http.response.body",
                "body": body_chunk,
            }
        )
