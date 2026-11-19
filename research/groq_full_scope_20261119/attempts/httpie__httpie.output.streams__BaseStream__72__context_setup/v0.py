import pytest
from httpie.output.streams import BaseStream, DataSuppressedError
from httpie.models import HTTPMessage, OutputOptions
from httpie.encoding import UTF8


class DummyStream(BaseStream):
    """Concrete BaseStream for testing that yields predefined body chunks."""
    def __init__(self, msg, output_options, body_chunks, **kwargs):
        super().__init__(msg, output_options, **kwargs)
        self.body_chunks = body_chunks

    def iter_body(self):
        for chunk in self.body_chunks:
            yield chunk


def test_stream_with_headers_body_and_meta(tmp_path):
    """Verify that headers, body, and metadata are yielded in order."""
    msg = HTTPMessage(
        headers="Content-Type: text/plain",
        metadata="Status: 200 OK",
        body=b"Hello, world!"
    )
    output_options = OutputOptions(headers=True, body=True, meta=True)
    stream = DummyStream(msg, output_options, [b"Hello, ", b"world!"])

    result = b"".join(stream)
    expected = (
        b"Content-Type: text/plain\r\n\r\n"
        b"Hello, world!"
        b"\n\n"
        b"Status: 200 OK\r\n\r\n"
    )
    assert result == expected


def test_on_body_chunk_downloaded_called(tmp_path):
    """Ensure the callback is invoked for each body chunk."""
    msg = HTTPMessage(headers="X-Test: 1", metadata="Meta", body=b"abc")
    output_options = OutputOptions(headers=True, body=True, meta=False)
    called_chunks = []

    def callback(chunk):
        called_chunks.append(chunk)

    stream = DummyStream(msg, output_options, [b"a", b"b", b"c"], on_body_chunk_downloaded=callback)
    list(stream)  # exhaust iterator

    assert called_chunks == [b"a", b"b", b"c"]


def test_data_suppressed_error_handling(tmp_path):
    """When iter_body raises DataSuppressedError, the stream yields the error message."""
    class ErrorStream(BaseStream):
        def iter_body(self):
            raise DataSuppressedError("Body suppressed due to size")

    msg = HTTPMessage(headers="X-Info: test", metadata="Meta", body=b"")
    output_options = OutputOptions(headers=True, body=True, meta=True)
    stream = ErrorStream(msg, output_options)

    result = b"".join(stream)
    expected = (
        b"X-Info: test\r\n\r\n"
        b"\n"
        b"Body suppressed due to size"
        b"\n\n"
        b"Meta\r\n\r\n"
    )
    assert result == expected
