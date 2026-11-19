import pytest
from httpie.output.streams import BufferedPrettyStream, BinarySuppressedError
from httpie.encoding import UTF8
from httpie.context import Environment
from httpie.models import HTTPMessage, OutputOptions
from httpie.processing import Conversion, Formatting


class DummyMessage(HTTPMessage):
    def __init__(self, body_chunks, content_type="text/plain"):
        self._body_chunks = body_chunks
        self.content_type = content_type
        self.headers = {}
        self.metadata = {}

    def iter_body(self, chunk_size):
        for chunk in self._body_chunks:
            yield chunk

    def iter_lines(self, chunk_size):
        for chunk in self._body_chunks:
            yield chunk, b"\n"


class DummyConverter:
    def __init__(self, new_mime="text/plain"):
        self.new_mime = new_mime

    def convert(self, body_bytes):
        # pretend to decode bytes to a string
        return self.new_mime, body_bytes.decode("utf-8")


class DummyFormatting(Formatting):
    def format_headers(self, headers):
        return ""

    def format_metadata(self, metadata):
        return ""

    def format_body(self, content, mime):
        # identity formatting
        return content


class DummyConversion(Conversion):
    def __init__(self, converter=None):
        self._converter = converter

    def get_converter(self, mime):
        return self._converter


def test_buffered_pretty_stream_normal_text(tmp_path):
    body = [b"hello ", b"world"]
    msg = DummyMessage(body)
    conv = DummyConversion()
    fmt = DummyFormatting()
    stream = BufferedPrettyStream(
        conversion=conv,
        formatting=fmt,
        msg=msg,
        env=Environment(stdout_isatty=False),
        output_encoding=UTF8,
    )
    result = b"".join(stream.iter_body())
    assert result == b"hello world"


def test_buffered_pretty_stream_binary_raises():
    body = [b"binary\x00data"]
    msg = DummyMessage(body)
    conv = DummyConversion()
    fmt = DummyFormatting()
    stream = BufferedPrettyStream(
        conversion=conv,
        formatting=fmt,
        msg=msg,
        env=Environment(stdout_isatty=False),
        output_encoding=UTF8,
    )
    with pytest.raises(BinarySuppressedError):
        list(stream.iter_body())


def test_buffered_pretty_stream_conversion_on_binary(tmp_path):
    body = [b"binary\x00data"]
    msg = DummyMessage(body)
    conv = DummyConversion(DummyConverter(new_mime="text/plain"))
    fmt = DummyFormatting()
    stream = BufferedPrettyStream(
        conversion=conv,
        formatting=fmt,
        msg=msg,
        env=Environment(stdout_isatty=False),
        output_encoding=UTF8,
    )
    result = b"".join(stream.iter_body())
    assert result == b"binarydata"
