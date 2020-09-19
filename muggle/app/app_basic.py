import webob

from muggle.body import BinaryBody
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