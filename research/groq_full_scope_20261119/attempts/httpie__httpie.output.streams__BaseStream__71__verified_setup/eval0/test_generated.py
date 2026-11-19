import pytest
from httpie.output.streams import BaseStream
from httpie.models import HTTPMessage, OutputOptions
from httpie.output.processing import DataSuppressedError


class DummyStream(BaseStream):
    """Concrete implementation of BaseStream for testing."""

    def __init__(self, msg, output_options, body_chunks, **kwargs):
        super().__init__(msg, output_options, **kwargs)
        self.body_chunks = body_chunks

    def iter_body(self):
        for chunk in self.body_chunks:
            yield chunk


def test_headers_and_body_output():
    """Verify that headers and body are yielded in correct order."""
    msg = HTTPMessage(
        headers="Content-Type: text/plain\r\n",
        metadata="--metadata--",
        body=b"Hello, world!"
    )
    output_options = OutputOptions(headers=True, body=True, meta=False)
    stream = DummyStream(msg, output_options, [b"Hello, ", b"world!"])
    result = b"".join(stream)
    expected = (
        b"Content-Type: text/plain\r\n\r\n"
        b"Hello, world!"
    )
    assert result == expected


def test_body_suppressed_error():
    """Verify that a DataSuppressedError is handled correctly."""
    msg = HTTPMessage(
        headers="Content-Type: text/plain\r\n",
        metadata="--metadata--",
        body=b"Secret data"
    )
    output_options = OutputOptions(headers=True, body=True, meta=False)

    class SuppressStream(BaseStream):
        def iter_body(self):
            raise DataSuppressedError("Data suppressed")

    stream = SuppressStream(msg, output_options)
    result = b"".join(stream)
    expected = (
        b"Content-Type: text/plain\r\n\r\n"
        b"\n"
        b"Data suppressed"
    )
    assert result == expected


def test_metadata_output_with_body():
    """Verify that metadata is yielded after body with proper separators."""
    msg = HTTPMessage(
        headers="Content-Type: text/plain\r\n",
        metadata="--metadata--",
        body=b"Hello"
    )
    output_options = OutputOptions(headers=False, body=True, meta=True)
    stream = DummyStream(msg, output_options, [b"Hello"])
    result = b"".join(stream)
    expected = (
        b"Hello"
        b"\n\n"
        b"--metadata--"
        b"\n\n"
    )
    assert result == expected
