import pytest
from multidict import MultiDict, CIMultiDict

from muggle.rq.rq_without_header import RqWithoutHeaders
from test.test_mg_fork import FakeRequest


@pytest.mark.asyncio
async def test_rq_without_headers_immutability():
    headers = await RqWithoutHeaders(
        FakeRequest(
            headers=CIMultiDict({"foo": "bar", "accept": "some-value"}),
        ),
        ["foo"],
    ).headers()
    with pytest.raises(TypeError):
        headers["accept"] = "foo"


@pytest.mark.asyncio
async def test_rq_without_headers_case_insensitive():
    headers = await RqWithoutHeaders(
        FakeRequest(
            headers=MultiDict({"Foo": "bar", "accept": "some-value"}),
        ),
        ["ACCEPT"],
    ).headers()
    assert headers.getall("foo") == headers.getall("Foo") == ["bar"]
    assert "accept" not in headers
    assert "Accept" not in headers
