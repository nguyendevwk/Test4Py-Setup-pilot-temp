import pytest
from httpie.output.streams import BufferedPrettyStream, BinarySuppressedError
from httpie.encoding import UTF8
from httpie.models import HTTPMessage, OutputOptions
from httpie.processing import Conversion, Formatting
from httpie.context import Environment


class DummyMessage(HTTPMessage):
    """A minimal HTTPMessage that yields predefined body chunks."""
    def __init__(self, body_chunks, content_type="text/plain"):
        self._body_chunks = body_chunks
        self.content_type = content_type
        self.headers = {}
        self.metadata = {}
        self.encoding = "utf-8"

    def iter_body(self, chunk_size):
        for chunk in self._body_chunks:
            yield chunk


class DummyConverter:
    """A converter that turns bytes into a string and changes mime."""
    def convert(self, body_bytes):
        return "text/plain", body_bytes.decode("utf-8")


class DummyFormatting(Formatting):
    """Formatting that returns the body unchanged."""
    def format_body(self, content, mime):
        return content

    def format_headers(self, headers):
        return ""

    def format_metadata(self, metadata):
        return ""


class DummyConversion(Conversion):
    """Conversion that returns a DummyConverter for a specific mime."""
    def get_converter(self, mime):
        return DummyConverter() if mime == "application/octet-stream" else None


def test_buffered_pretty_stream_normal_body(tmp_path):
    """Body without null bytes should be processed normally."""
    body = b"Hello, world!"
    msg = DummyMessage([body])
    stream = BufferedPrettyStream(
        conversion=DummyConversion(),
        formatting=DummyFormatting(),
        msg=msg,
        env=Environment(stdout_isatty=False),
    )
    chunks = list(stream.iter_body())
    assert chunks == [b"Hello, world!"]


def test_buffered_pretty_stream_binary_body_raises():
    """Body containing a null byte should raise BinarySuppressedError."""
    body = b"binary\x00data"
    msg = DummyMessage([body])
    stream = BufferedPrettyStream(
        conversion=DummyConversion(),
        formatting=DummyFormatting(),
        msg=msg,
        env=Environment(stdout_isatty=False),
    )
    with pytest.raises(BinarySuppressedError):
        list(stream.iter_body())


def test_buffered_pretty_stream_conversion(tmp_path):
    """Body with a null byte triggers conversion and returns converted text."""
    body = b"binary\x00data"
    msg = DummyMessage([body], content_type="application/octet-stream")
    stream = BufferedPrettyStream(
        conversion=DummyConversion(),
        formatting=DummyFormatting(),
        msg=msg,
        env=Environment(stdout_isatty=False),
    )
    chunks = list(stream.iter_body())
    assert chunks == [b"binarydata"]  # converter removes null and decodes
