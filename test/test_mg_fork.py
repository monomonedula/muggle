import re
from types import MappingProxyType
from typing import AsyncIterator, Mapping, Optional
from urllib.parse import urlparse, ParseResult

import pytest
from multidict import MultiMapping

from muggle.facets.fk.fk_regex import FkRegex
from muggle.facets.fk.mg_fork import MgFork
from muggle.http_exception import HttpException
from muggle.request import Request
from muggle.response import Response
from muggle.rs.rs_text import RsText


class FakeRequest(Request):
    def __init__(self, url: str = "/hello-world?foo=bar", method: str = "GET",
                 headers: Mapping[str, str] = MappingProxyType({"Foo": "bar"}), body: Optional[bytes] = None):
        self._url: str = url
        self._method: str = method
        self._headers: Mapping[str, str] = headers
        self._body: Optional[bytes] = body

    async def headers(self) -> MultiMapping[str, str]:
        return self._headers

    async def uri(self) -> ParseResult:
        return urlparse(self._url)

    async def method(self) -> str:
        return self._method

    async def body(self) -> AsyncIterator[bytes]:
        if self._body is None:
            return
        yield self._body

    def __repr__(self):
        return f"FakeRequest[{self._url}, {self._method}, {self._headers}, {self._body}]"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "rq, expected_response",
    [
        [FakeRequest("/foo-bar"), RsText(text="resp1")],
        [FakeRequest("/hello-world"), RsText(text="resp2")],
        [FakeRequest("/hello-friend"), RsText(text="resp3")],
        [FakeRequest("/bang7"), RsText(text="resp4")],
    ]
)
async def test_mg_fork_with_fk_regex(rq, expected_response):
    resp: Optional[Response] = await MgFork(
        FkRegex(pattern="/foo-bar", resp=RsText(text="resp1")),
        FkRegex(pattern="/hello-world", resp=RsText(text="resp2")),
        FkRegex(pattern="/hello.*", resp=RsText(text="resp3")),
        FkRegex(pattern=re.compile("/bang[0-9]"), resp=RsText(text="resp4")),
        FkRegex(pattern="/foo-baz", resp=RsText(text="resp5")),
    ).act(rq)
    if expected_response is None:
        assert resp is None
    else:
        assert resp is not None
        assert await resp.body().__anext__() == await expected_response.body().__anext__()
        assert await resp.status() == await expected_response.status()
        assert await resp.headers() == await expected_response.headers()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "rq",
    [
        FakeRequest("/some-unexpected-path"),
        FakeRequest("hello-world"),
    ]
)
async def test_mg_fork_raises(rq):
    with pytest.raises(HttpException) as e:
        await MgFork(
            FkRegex(pattern="/foo-bar", resp=RsText(text="resp1")),
            FkRegex(pattern="/hello-world", resp=RsText(text="resp2")),
        ).act(rq)
    assert e.value.code() == 404
