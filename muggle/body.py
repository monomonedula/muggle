import io
from abc import ABC, abstractmethod
from typing import TextIO, Union, BinaryIO


class Body(ABC):
    @abstractmethod
    def body(self) -> BinaryIO:
        pass


class TextBody(Body):
    def __init__(self, text: Union[str, bytes, TextIO]):
        if isinstance(text, str):
            body = lambda: io.BytesIO(text.encode())
        elif isinstance(text, bytes):
            body = lambda: io.BytesIO(text)
        elif isinstance(text, io.TextIOBase):
            body = lambda: BytesIOWrapper(text)
        else:
            raise TypeError("Expected Union[str, bytes, TextIO] got %r" % type(text))
        self._body = body

    def body(self) -> BinaryIO:
        return self._body()


class BinaryBody(Body):
    def __init__(self, body: BinaryIO):
        self._body = body

    def body(self) -> BinaryIO:
        return self._body


class BytesIOWrapper(io.BufferedReader):
    """Wrap a buffered bytes stream over TextIOBase string stream."""

    def __init__(self, text_io_buffer, encoding=None, errors=None, **kwargs):
        super(BytesIOWrapper, self).__init__(text_io_buffer, **kwargs)
        self.encoding = encoding or text_io_buffer.encoding or "utf-8"
        self.errors = errors or text_io_buffer.errors or "strict"

    def _encoding_call(self, method_name, *args, **kwargs):
        raw_method = getattr(self.raw, method_name)
        val = raw_method(*args, **kwargs)
        return val.encode(self.encoding, errors=self.errors)

    def read(self, size=-1):
        return self._encoding_call("read", size)

    def read1(self, size=-1):
        return self._encoding_call("read1", size)

    def peek(self, size=-1):
        return self._encoding_call("peek", size)
