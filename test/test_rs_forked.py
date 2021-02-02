from typing import Optional, AsyncIterator, Dict

from muggle.fk.fk_regex import ResponseForked, FkRegex
from muggle.fork import Fork
from muggle.request import Request
from muggle.response import Response
from muggle.rs.rs_text import RsText


class FakeRequest(Request):
    async def headers(self) -> Dict[str, str]:
        return {"Foo": "bar"}

    async def uri(self) -> str:
        return "/hello-world?foo=bar"

    async def method(self) -> str:
        return "GET"

    async def body(self) -> AsyncIterator[bytes]:
        return
        yield


async def test_rs_forked():
    ResponseForked(
        FkRegex(pattern="/foo-bar", resp=RsText(text="foo-bar")),
        FkRegex(pattern="/foo-bar", resp=RsText(text="foo-bar")),
    )
