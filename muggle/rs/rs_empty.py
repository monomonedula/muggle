import io
from typing import Dict, BinaryIO

from muggle.response import Response


class RsEmpty(Response):
    def status(self) -> str:
        return "204 No Content"

    def headers(self) -> Dict[str, str]:
        return {}

    def body(self) -> BinaryIO:
        return io.BytesIO()
