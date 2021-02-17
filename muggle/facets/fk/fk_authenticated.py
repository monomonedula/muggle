from typing import Optional

from muggle.fork import Fork
from muggle.request import Request
from muggle.response import Response


class FkAuthenticated(Fork):
    async def route(self, request: Request) -> Optional[Response]:
        pass
