from typing import Dict, Union, Optional

from abc_delegation import delegation_metaclass

from muggle.primitives.scalar import Scalar, scalar_copied
from muggle.response import Response


class RsWithHeaders(Response, metaclass=delegation_metaclass("_response")):
    def __init__(self, resp: Response, headers: Union[Dict[str, str], Scalar[Dict[str, str]]]):
        self._response: Response = resp
        self._headers: Scalar[Dict[str, str]]
        if isinstance(headers, Scalar):
            self._headers = headers
        else:
            self._headers = scalar_copied(headers)

    def headers(self) -> Scalar[Dict[str, str]]:
        return AlteredHeaders(
            self._response.headers(),
            update=self._headers,
        )


class AlteredHeaders(Scalar[Dict[str, str]]):
    def __init__(
        self, origin: Scalar[Dict[str, str]],
        update: Optional[Scalar[Dict[str, str]]] = None,
        to_remove: Optional[Scalar[Dict[str, str]]] = None,
    ):
        self.__headers: Scalar[Dict[str, str]] = origin
        self.__upd: Optional[Scalar[Dict[str, str]]] = update
        self.__to_remove: Optional[Scalar[Dict[str, str]]] = to_remove

    async def value(self) -> Dict[str, str]:
        headers = await self.__headers.value()
        if self.__upd is not None:
            headers.update(await self.__upd.value())
        if self.__to_remove is not None:
            to_remove = await self.__to_remove.value()
            for h in to_remove:
                headers.pop(h, None)
        return headers
