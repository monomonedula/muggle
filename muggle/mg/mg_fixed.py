from muggle.muggle import Muggle
from muggle.request import Request
from muggle.response import Response


class MgFixed(Muggle):
    def __init__(self, resp: Response):
        self._response = resp

    def act(self, request: "Request") -> "Response":
        return self._response
