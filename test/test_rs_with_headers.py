import pytest
from multidict import CIMultiDict, MultiDict

from muggle.rs.rs_fake import RsFake
from muggle.rs.rs_with_header import RsWithHeaders


@pytest.mark.asyncio
async def test_rs_with_headers_immutability():
    headers = await RsWithHeaders(
        RsFake(
            "200 OK",
            CIMultiDict({"foo": "bar", "accept": "some-value"}),
        ),
        {"foo": "baz"},
    ).headers()
    with pytest.raises(TypeError):
        headers["accept"] = "foo"


@pytest.mark.asyncio
async def test_rs_with_headers_case_insensitive():
    headers = await RsWithHeaders(
        RsFake(
            "200 OK",
            MultiDict({"Foo": "bar", "accept": "some-value"}),
        ),
        {"foo": "baz"},
    ).headers()
    assert headers.getall("foo") == headers.getall("Foo") == ["bar", "baz"]
    assert headers.getall("accept") == headers.getall("ACCEPT") == ["some-value"]


@pytest.mark.asyncio
async def test_rs_with_headers_headers_value():
    assert (
        sorted(
            (
                await RsWithHeaders(
                    RsFake(
                        "200 OK",
                        CIMultiDict({"foo": "bar", "accept": "some-value"}),
                    ),
                    {"foo": "baz"},
                ).headers()
            ).items()
        )
        == [("accept", "some-value"), ("foo", "bar"), ("foo", "baz")]
    )
