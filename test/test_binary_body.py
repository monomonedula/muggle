import tempfile

import pytest

from muggle.body import BinaryBody


@pytest.mark.asyncio
async def test_binary_body_iter():
    tmp = tempfile.TemporaryFile(mode="w+b")
    tmp.write(b"Foo")
    tmp.seek(0)
    bb = BinaryBody(tmp)
    assert await bb.body().__anext__() == b"Foo"
    assert await bb.body().__anext__() == b""
    tmp.seek(0)
    assert await bb.body().__anext__() == b"Foo"
