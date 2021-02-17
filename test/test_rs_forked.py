from typing import AsyncIterator, Dict
from urllib.parse import urlparse, ParseResult

from multidict import MultiMapping, MultiDict

from muggle.facets.fk.fk_regex import ResponseForked, FkRegex
from muggle.facets.fk.mg_fork import MgFork
from muggle.request import Request
from muggle.rs.rs_text import RsText


class FakeRequest(Request):
    async def headers(self) -> MultiMapping[str, str]:
        return MultiDict({"Foo": "bar"})

    async def uri(self) -> ParseResult:
        return urlparse("/hello-world?foo=bar")

    async def method(self) -> str:
        return "GET"

    async def body(self) -> AsyncIterator[bytes]:
        return
        yield


async def test_rs_forked():
    MgFork(
        FkRegex(pattern="/foo-bar", resp=RsText(text="foo-bar")),
        FkRegex(pattern="/foo-bar", resp=RsText(text="foo-bar")),
    )
