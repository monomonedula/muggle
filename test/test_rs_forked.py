from typing import Optional, AsyncIterator, Dict

from muggle.fk.fk_regex import ResponseForked, FkRegex
from muggle.fork import Fork
from muggle.primitives.scalar import Scalar, scalar
from muggle.request import Request
from muggle.response import Response
from muggle.rs.rs_text import RsText


class FakeRequest(Request):
    def headers(self) -> Scalar[Dict[str, str]]:
        return scalar(
            {"Foo": "bar"}
        )

    def uri(self) -> Scalar[str]:
        return scalar("/hello-world?foo=bar")

    def method(self) -> Scalar[str]:
        return scalar("GET")

    async def body(self) -> AsyncIterator[bytes]:
        return
        yield


async def test_rs_forked():
    ResponseForked(
        FkRegex(
            pattern="/foo-bar",
            resp=RsText(
                text="foo-bar"
            )
        ),
        FkRegex(
            pattern="/foo-bar",
            resp=RsText(
                text="foo-bar"
            )
        )

    )