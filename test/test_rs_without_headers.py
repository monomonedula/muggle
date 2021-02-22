import pytest
from multidict import CIMultiDict, MultiDict

from muggle.rs.rs_fake import RsFake
from muggle.rs.rs_without_header import RsWithoutHeaders


@pytest.mark.asyncio
async def test_rs_without_headers_immutability():
    headers = await RsWithoutHeaders(
        RsFake(
            "200 OK",
            CIMultiDict({"foo": "bar", "accept": "some-value"}),
        ),
        ["accept"],
    ).headers()
    with pytest.raises(TypeError):
        headers["accept"] = "foo"


@pytest.mark.asyncio
async def test_rs_without_headers_case_insensitive():
    headers = await RsWithoutHeaders(
        RsFake(
            "200 OK",
            MultiDict({"foo": "bar", "Accept": "some-value"}),
        ),
        ["accept"],
    ).headers()
    assert headers["foo"] == headers["Foo"] == "bar"
    assert "accept" not in headers
    assert "Accept" not in headers


@pytest.mark.asyncio
async def test_rs_without_headers_headers():
    assert (
        sorted(
            (
                await RsWithoutHeaders(
                    RsFake(
                        status="200 OK",
                        headers=CIMultiDict(
                            {
                                "Accept": "Some-Value",
                                "Hello": "Another-Value",
                                "Foo": "Bar",
                            }
                        ),
                    ),
                    ["Hello", "Accept", "Missing"],
                ).headers()
            ).items()
        )
        == [("Foo", "Bar")]
    )
