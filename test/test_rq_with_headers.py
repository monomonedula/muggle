import pytest
from multidict import MultiDict, CIMultiDict

from muggle.rq.rq_with_headers import RqWithHeaders
from test.test_mg_fork import FakeRequest


@pytest.mark.asyncio
async def test_rq_with_headers_immutability():
    headers = await RqWithHeaders(
        FakeRequest(
            headers=CIMultiDict({"foo": "bar", "accept": "some-value"}),
        ),
        {"foo": "baz"},
    ).headers()
    with pytest.raises(TypeError):
        headers["accept"] = "foo"


@pytest.mark.asyncio
async def test_rq_with_headers_case_insensitive():
    headers = await RqWithHeaders(
        FakeRequest(
            headers=MultiDict({"Foo": "bar", "accept": "some-value"}),
        ),
        {"foo": "baz"},
    ).headers()
    assert headers.getall("foo") == headers.getall("Foo") == ["bar", "baz"]
    assert headers.getall("accept") == headers.getall("ACCEPT") == ["some-value"]
