import pytest
from multidict import CIMultiDict

from muggle.rs.rs_fake import RsFake
from muggle.rs.rs_text import RsText
from muggle.rs.rs_with_header import RsWithHeaders
from muggle.rs.rs_with_status import RsWithStatus


@pytest.mark.asyncio
async def test_rs_with_status_status():
    assert await RsWithStatus(200, "Whatever").status() == "200 Whatever"


@pytest.mark.asyncio
async def test_rs_with_status_reason():
    assert await RsWithStatus(404).status() == "404 Not Found"


@pytest.mark.parametrize("status", [99, 0, -10, 1000])
def test_rs_with_status_bad_status(status):
    with pytest.raises(TypeError):
        RsWithStatus(status)


@pytest.mark.asyncio
async def test_rs_with_status_empty():
    rs = RsWithStatus(404)
    with pytest.raises(StopAsyncIteration):
        await rs.body().__anext__()

    assert await rs.headers() == CIMultiDict()


@pytest.mark.asyncio
async def test_rs_with_status_decorating():
    rs = RsWithStatus(
        404,
        response=RsFake(
            status="200 OK", body=b"foo bar", headers=CIMultiDict({"Hello": "there"})
        ),
    )
    assert await rs.body().__anext__() == b"foo bar"
    assert await rs.headers() == CIMultiDict({"Hello": "there"})
    assert await rs.status() == "404 Not Found"
