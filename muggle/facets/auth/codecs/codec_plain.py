from typing import List, Dict
from urllib.parse import quote, unquote

from muggle.facets.auth.codecs.codec import Codec
from muggle.facets.auth.identity import Identity, IdentitySimple


class CcPlain(Codec):
    async def encode(self, identity: Identity) -> bytes:
        parts = [
            await identity.urn(),
            *[f";{key}={quote(value)}" for key, value in await identity.properties()],
        ]
        return "".join(parts).encode()

    async def decode(self, bts: bytes) -> Identity:
        props: Dict[str, str] = {}
        parts: List[str] = bts.decode().split(";")
        for p in parts[1:]:
            k, v = p.split("=")
            props[k] = unquote(v)
        return IdentitySimple(unquote(parts[0]), props)
