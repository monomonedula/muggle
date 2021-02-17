from typing import Optional, Tuple

from muggle.fork import Fork
from muggle.request import Request
from muggle.response import Response


class FkChain(Fork):
    def __init__(self, *forks: Fork):
        self._forks: Tuple[Fork, ...] = forks

    async def route(self, request: Request) -> Optional[Response]:
        for fork in self._forks:
            rs = fork.route(request)
            if rs is not None:
                return rs
