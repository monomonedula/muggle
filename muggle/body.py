import io
from abc import ABC, abstractmethod
from typing import TextIO, Union, AsyncIterator, Callable, cast, IO


class Body(ABC):
    @abstractmethod
    def body(self) -> AsyncIterator[bytes]:
        pass


class TextBody(Body):
    def __init__(self, text: Union[str, bytes, TextIO]):
        body: Callable[[], bytes]
        if isinstance(text, str):

            def body() -> bytes:
                return cast(str, text).encode()

        elif isinstance(text, bytes):

            def body() -> bytes:
                return cast(bytes, text)

        elif isinstance(text, io.TextIOBase):

            def body() -> bytes:
                return cast(io.TextIOBase, text).read().encode()

        else:
            raise TypeError("Expected Union[str, bytes, TextIO] got %r" % type(text))
        self._body: Callable[[], bytes] = body

    async def body(self) -> AsyncIterator[bytes]:
        yield self._body()


class BinaryBody(Body):
    def __init__(self, body: IO[bytes]):
        self._body: IO[bytes] = body

    async def body(self) -> AsyncIterator[bytes]:
        yield self._body.read()


class BodyFromASGI(Body):
    def __init__(self, receive):
        self._receive = receive

    async def body(self) -> AsyncIterator[bytes]:
        more_body = True
        while more_body:
            message = await self._receive()
            yield message.get("body", b"")
            more_body = message.get("more_body", False)
