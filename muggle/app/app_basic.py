import webob

from muggle.body import BinaryBody, BodyFromASGI
from muggle.headofrequest import SimpleHeadOfRequest
from muggle.http_exception import HttpException
from muggle.muggle import Muggle
from muggle.rq.rq_of import RqOf
from muggle.rs.rs_with_status import RsWithStatus


class AppBasic:
    def __init__(self, muggle: Muggle):
        self._muggle = muggle

    def __call__(self, environ, start_response):
        rq = webob.Request(environ)
        try:
            response = self._muggle.act(
                RqOf(SimpleHeadOfRequest(rq.headers.items(), environ["RAW_URI"], rq.method), BinaryBody(rq.body_file))
            )
        except HttpException as e:
            response = RsWithStatus(e.code())
        start_response(response.status(), headers=response.headers().items())
        return iter(response.body())


class AppBasic2:
    def __init__(self, muggle: Muggle):
        self._muggle = muggle

    async def __call__(self, scope, receive, send):
        try:
            response = self._muggle.act(
                RqOf(
                    SimpleHeadOfRequest(
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


def headers(scope):
    return {name: value for name, value in scope["headers"]}
