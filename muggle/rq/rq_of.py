from typing import Dict, BinaryIO

from muggle.body import Body
from muggle.headofrequest import HeadOfRequest
from muggle.request import Request


class RqOf(Request):
    def __init__(self, head: HeadOfRequest, body: Body):
        self._body = body
        self._head = head

    def headers(self) -> Dict[str, str]:
        return self._head.headers()

    def body(self) -> BinaryIO:
        return self._body.body()

    def uri(self) -> str:
        return self._head.uri()

    def method(self) -> str:
        return self._head.method()
