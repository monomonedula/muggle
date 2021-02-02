from muggle.fork import Fork
from muggle.http_exception import HttpException
from muggle.muggle import Muggle
from muggle.request import Request
from muggle.response import Response


class MgFork(Muggle):
    def __init__(self, fork: Fork):
        self._fork: Fork = fork

    def act(self, request: Request) -> Response:
        response: Response = await self._fork.route(request)
        if response:
            return response
        raise HttpException(404)
