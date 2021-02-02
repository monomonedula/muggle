from muggle.body import BodyFromASGI
from muggle.headrq import SimpleHeadRq
from muggle.http_exception import HttpException
from muggle.muggle import Muggle
from muggle.rq.rq_of import RqOf
from muggle.rs.rs_with_status import RsWithStatus


class AppBasic:
    def __init__(self, muggle: Muggle):
        self._muggle: Muggle = muggle

    async def __call__(self, scope, receive, send):
        try:
            response = self._muggle.act(
                RqOf(
                    SimpleHeadRq(
                        headers(scope), scope["path"], scope["method"]
                    ),
                    BodyFromASGI(receive)
                )
            )
        except HttpException as e:
            response = RsWithStatus(e.code())
        await send(
            {
                "type": "http.response.start",
                "status": await response.status().value(),
                "headers": await response.headers().value(),
            }
        )
        async for body_chunk in response.body():
            await send(
                {
                    "type": "http.response.body",
                    "body": body_chunk,
                }
            )


def headers(scope):
    return {name: value for name, value in scope["headers"]}
