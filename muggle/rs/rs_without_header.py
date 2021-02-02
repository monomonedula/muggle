from typing import Dict, Union

from abc_delegation import delegation_metaclass

from muggle.primitives.scalar import Scalar, scalar
from muggle.response import Response
from muggle.rs.rs_with_header import AlteredHeaders


class RsWithoutHeaders(Response, metaclass=delegation_metaclass("_response")):
    def __init__(self, resp: Response, headers: Union[Dict[str, str], Scalar[Dict[str, str]]]):
        self._response = resp
        if isinstance(headers, Scalar):
            self._headers = headers
        else:
            self._headers = scalar(headers)

    def headers(self) -> Scalar[Dict[str, str]]:
        return AlteredHeaders(
            self._response.headers(),
            to_remove=self._headers
        )
