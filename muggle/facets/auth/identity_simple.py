from types import MappingProxyType
from typing import Mapping, Optional

from muggle.facets.auth.identity import Identity


class IdSimple(Identity):
    def __init__(self, urn: str, props: Optional[Mapping[str, str]] = None):
        self._urn: str = urn
        self._props: Mapping[str, str] = (
            MappingProxyType({}) if props is None else props
        )

    async def urn(self) -> str:
        return self._urn

    async def properties(self) -> Mapping[str, str]:
        return self._props
