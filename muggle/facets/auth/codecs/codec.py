from abc import ABC, abstractmethod

from muggle.facets.auth.identity import Identity


class Codec(ABC):
    @abstractmethod
    async def encode(self, identity: Identity) -> bytes:
        pass

    @abstractmethod
    async def decode(self, bts: bytes) -> Identity:
        pass
