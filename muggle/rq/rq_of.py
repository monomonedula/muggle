from typing import Dict, AsyncGenerator, Awaitable, AsyncIterator

from muggle.body import Body
from muggle.headrq import HeadRq
from muggle.primitives.scalar import Scalar
from muggle.request import Request


class RqOf(Request):
    def __init__(self, head: HeadRq, body: Body):
        self._body = body
        self._head = head

    def headers(self) -> Scalar[Dict[str, str]]:
        return self._head.headers()

    def body(self) -> AsyncIterator[bytes]:
        return self._body.body()

    def uri(self) -> Scalar[str]:
        return self._head.uri()

    def method(self) -> Scalar[str]:
        return self._head.method()
