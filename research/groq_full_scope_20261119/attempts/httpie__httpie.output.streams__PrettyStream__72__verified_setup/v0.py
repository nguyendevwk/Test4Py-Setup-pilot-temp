import pytest
from httpie.output.streams import PrettyStream, BinarySuppressedError
from httpie.encoding import UTF8
from httpie.models import HTTPMessage, OutputOptions
from httpie.processing import Conversion, Formatting
from httpie.context import Environment


class DummyConversion(Conversion):
    def get_converter(self, mime):
        # Converter that simply decodes bytes to string and returns same mime
        return self

    def convert(self, body: bytes):
        return "text/plain", body.decode("utf-8")


class DummyFormatting(Formatting):
    def format_headers(self, headers):
        return "Headers: " + ", ".join(f"{k}: {v}" for k, v in headers.items())

    def format_metadata(self, metadata):
        return "Metadata: " + ", ".join(f"{k}: {v}" for k, v in metadata.items())

    def format_body(self, content, mime):
        # For simplicity, just return content unchanged
        return content


def make_message(body_lines, headers=None, metadata=None):
    headers = headers or {}
    metadata = metadata or {}
    # HTTPMessage expects a file-like object; we simulate with a simple class
    class Msg(HTTPMessage):
        def __init__(self, lines, headers, metadata):
            self._lines = lines
            self.headers = headers
            self.metadata = metadata

        def iter_lines(self, chunk_size):
            for line in self._lines:
                yield line, b"\n"

    return Msg(body_lines, headers, metadata)


def test_pretty_stream_normal_lines(tmp_path):
    msg = make_message([b"line1", b"line2", b"line3"])
    stream = PrettyStream(
        conversion=DummyConversion(),
        formatting=DummyFormatting(),
        msg=msg,
        output_encoding=UTF8,
        mime="text/plain",
        env=Environment(),
    )
    output = list(stream.iter_body())
    assert output == [b"line1\n", b"line2\n", b"line3\n"]


def test_pretty_stream_null_in_first_chunk(tmp_path):
    msg = make_message([b"data with null \0 byte", b"rest"])
    stream = PrettyStream(
        conversion=DummyConversion(),
        formatting=DummyFormatting(),
        msg=msg,
        output_encoding=UTF8,
        mime="application/octet-stream",
        env=Environment(),
    )
    output = list(stream.iter_body())
    # Converter should produce a single string "data with null  byte rest"
    assert output == [b"data with null  byte rest"]


def test_pretty_stream_null_after_first_chunk_raises(tmp_path):
    msg = make_message([b"first line", b"second line with \0 null"])
    stream = PrettyStream(
        conversion=DummyConversion(),
        formatting=DummyFormatting(),
        msg=msg,
        output_encoding=UTF8,
        mime="text/plain",
        env=Environment(),
    )
    with pytest.raises(BinarySuppressedError):
        list(stream.iter_body())
