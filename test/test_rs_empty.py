import pytest

from muggle.rs.rs_empty import RsEmpty


@pytest.mark.asyncio
async def test_rs_empty():
    rs = RsEmpty()
    assert await rs.headers() == {}
    assert await rs.status() == "204 No Content"
    async for _ in rs.body():
        assert False
