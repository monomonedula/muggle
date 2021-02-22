from typing import Union

from io import StringIO

import pytest

from muggle.body import TextBody


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "s", ["Test string 1", b"Test string 1", StringIO("Test string 1")]
)
async def test_text_body_from_iteration(s: Union[str, bytes, StringIO]):
    body = TextBody(s)
    body_iter = body.body()
    assert await body_iter.__anext__() == b"Test string 1"
    with pytest.raises(StopAsyncIteration):
        await body_iter.__anext__()


@pytest.mark.asyncio
@pytest.mark.parametrize("s", ["Test string 1", b"Test string 1"])
async def test_text_body_from_iteration_reread(s: Union[str, bytes]):
    body = TextBody(s)
    assert await body.body().__anext__() == b"Test string 1"
    assert await body.body().__anext__() == b"Test string 1"


@pytest.mark.asyncio
async def test_text_body_from_iteration_reread_text_io():
    body = TextBody(StringIO("Test string 1"))
    assert await body.body().__anext__() == b"Test string 1"
    assert await body.body().__anext__() == b""


@pytest.mark.asyncio
async def test_text_body_from_bad_type():
    class Foo:
        def read(self):
            return ""
    with pytest.raises(TypeError):
        TextBody(Foo())     # type: ignore
