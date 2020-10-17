from typing import Dict, AsyncGenerator, Awaitable

from muggle.body import Body
from muggle.headofrequest import HeadOfRequest
from muggle.request import Request


class RqOf(Request):
    def __init__(self, head: HeadOfRequest, body: Body):
        self._body = body
        self._head = head

    def headers(self) -> Awaitable[Dict[str, str]]:
        return self._head.headers()

    def body(self) -> AsyncGenerator[bytes]:
        return self._body.body()

    def uri(self) -> Awaitable[str]:
        return self._head.uri()

    def method(self) -> Awaitable[str]:
        return self._head.method()
