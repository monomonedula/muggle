from typing import TextIO
import io

import pytest

from muggle.body import TextBody
from muggle.rs.rs_text import RsText
from muggle.rs.rs_with_header import RsWithHeaders
from muggle.rs.rs_with_status import RsWithStatus


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "text, expected_status, expected_headers, expected_text",
    [
        ("input text 1", "200 OK", {"Content-Type": "text/plain"}, b"input text 1"),
        (b"input text 2", "200 OK", {"Content-Type": "text/plain"}, b"input text 2"),
        (io.StringIO("input text 3"), "200 OK", {"Content-Type": "text/plain"}, b"input text 3"),
    ]
)
async def test_rs_text_str(text, expected_status, expected_headers, expected_text):
    rs = RsText(text)
    assert await rs.status().value() == "200 OK"
    assert await rs.headers().value() == {"Content-Type": "text/plain"}
    body = rs.body()
    assert await body.__anext__() == expected_text
    with pytest.raises(StopAsyncIteration):
        await body.__anext__()


@pytest.mark.asyncio
async def test_rs_text():
    rs = RsText(
        b"12345",
        RsWithHeaders(
            RsWithStatus(204),
            {"foo": "bar"}
        )
    )
    assert await rs.status().value() == "204 No Content"
    assert await rs.headers().value() == {"Content-Type": "text/plain", "foo": "bar"}
    body = rs.body()
    assert await body.__anext__() == b"12345"
    with pytest.raises(StopAsyncIteration):
        await body.__anext__()
