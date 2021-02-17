from typing import Tuple, Optional

from muggle.fork import Fork
from muggle.http_exception import HttpException
from muggle.muggle import Muggle
from muggle.request import Request
from muggle.response import Response


class MgFork(Muggle):
    def __init__(self, *forks: Fork):
        self._forks: Tuple[Fork, ...] = forks

    async def act(self, request: Request) -> Response:
        for fork in self._forks:
            response: Optional[Response] = await fork.route(request)
            if response is not None:
                return response
        raise HttpException(404)
