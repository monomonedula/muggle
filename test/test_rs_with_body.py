import pytest
from multidict import CIMultiDict

from muggle.body import TextBody
from muggle.rs.rs_fake import RsFake
from muggle.rs.rs_with_body import RsWithBody


@pytest.mark.asyncio
async def test_rs_with_body_body():
    assert (
        await RsWithBody(
            TextBody("New text"),
            RsFake("200 Whatever", body=b"Fake body"),
        )
        .body()
        .__anext__()
        == b"New text"
    )


@pytest.mark.asyncio
async def test_rs_with_body_transparent():
    rs = RsWithBody(
        TextBody("New text"),
        RsFake("200 Whatever", headers=CIMultiDict({"Hi": "Mark"}), body=b"Fake body"),
    )
    assert await rs.status() == "200 Whatever"
    assert await rs.headers() == CIMultiDict({"Hi": "Mark"})
