import pytest
from multidict import CIMultiDict

from muggle.rs.rs_fake import RsFake
from muggle.rs.rs_with_type import RsWithType, Json, Xml, Text, Html


@pytest.mark.asyncio
async def test_rs_with_type_headers():
    assert await RsWithType(
        RsFake(
            "201 CREATED",
            CIMultiDict({"foo": "bar", "accept": "some-value"}),
        ),
        type_="text/html",
    ).headers() == CIMultiDict(
        {"foo": "bar", "accept": "some-value", "content-type": "text/html"}
    )


@pytest.mark.asyncio
async def test_rs_with_type_headers_delete_previous():
    assert await RsWithType(
        RsFake(
            "201 CREATED",
            CIMultiDict(
                {
                    "foo": "bar",
                    "accept": "some-value",
                    "CONTENT-TYPE": "application/json",
                }
            ),
        ),
        type_="text/html",
    ).headers() == CIMultiDict(
        {"foo": "bar", "accept": "some-value", "content-type": "text/html"}
    )


@pytest.mark.asyncio
async def test_rs_with_type_headers_charset():
    assert await RsWithType(
        RsFake(
            "201 CREATED",
            CIMultiDict({"foo": "bar", "accept": "some-value"}),
        ),
        type_="whatever",
        charset="utf-8",
    ).headers() == CIMultiDict(
        {
            "foo": "bar",
            "accept": "some-value",
            "content-type": "whatever; charset=utf-8",
        }
    )


@pytest.mark.asyncio
async def test_json():
    assert await Json(
        RsFake(
            "201 CREATED",
            CIMultiDict({"foo": "bar", "accept": "some-value"}),
        ),
        charset="utf-8",
    ).headers() == CIMultiDict(
        {
            "foo": "bar",
            "accept": "some-value",
            "content-type": "application/json; charset=utf-8",
        }
    )


@pytest.mark.asyncio
async def test_html():
    assert await Html(
        RsFake(
            "201 CREATED",
            CIMultiDict({"foo": "bar", "accept": "some-value"}),
        ),
        charset="utf-8",
    ).headers() == CIMultiDict(
        {
            "foo": "bar",
            "accept": "some-value",
            "content-type": "text/html; charset=utf-8",
        }
    )


@pytest.mark.asyncio
async def test_text():
    assert await Text(
        RsFake(
            "201 CREATED",
            CIMultiDict({"foo": "bar", "accept": "some-value"}),
        ),
        charset="utf-8",
    ).headers() == CIMultiDict(
        {
            "foo": "bar",
            "accept": "some-value",
            "content-type": "text/plain; charset=utf-8",
        }
    )


@pytest.mark.asyncio
async def test_xml():
    assert await Xml(
        RsFake(
            "201 CREATED",
            CIMultiDict({"foo": "bar", "accept": "some-value"}),
        ),
        charset="utf-8",
    ).headers() == CIMultiDict(
        {
            "foo": "bar",
            "accept": "some-value",
            "content-type": "text/xml; charset=utf-8",
        }
    )
