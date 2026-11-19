import pytest
from httpie.output.streams import BaseStream
from httpie.models import HTTPMessage, OutputOptions
from httpie.output.processing import DataSuppressedError


class DummyStream(BaseStream):
    """Concrete BaseStream for testing that yields a fixed body."""
    def iter_body(self):
        return iter([b"part1", b"part2"])


class SuppressStream(BaseStream):
    """Concrete BaseStream that raises DataSuppressedError during body iteration."""
    def iter_body(self):
        raise DataSuppressedError(b"Suppressed content")


class MetaOnlyStream(BaseStream):
    """Concrete BaseStream that yields no body but provides metadata."""
    def iter_body(self):
        return iter([])


def test_normal_body_and_headers_and_meta(tmp_path):
    msg = HTTPMessage(
        headers="Content-Type: text/plain\r\n",
        metadata="Meta: value\r\n",
        body=b"Hello, world!"
    )
    opts = OutputOptions(headers=True, body=True, meta=True)
    stream = DummyStream(msg, opts)
    chunks = list(stream)
    # headers + double CRLF
    assert chunks[0] == b"Content-Type: text/plain\r\n"
    assert chunks[1] == b'\r\n\r\n'
    # body parts
    assert chunks[2] == b"part1"
    assert chunks[3] == b"part2"
    # meta separator and content
    assert chunks[4] == b'\n\n'
    assert chunks[5] == b"Meta: value\r\n"
    assert chunks[6] == b'\n\n'


def test_suppressed_body_with_headers(tmp_path):
    msg = HTTPMessage(
        headers="X-Test: 123\r\n",
        metadata="",
        body=b""
    )
    opts = OutputOptions(headers=True, body=True, meta=False)
    stream = SuppressStream(msg, opts)
    chunks = list(stream)
    # headers + double CRLF
    assert chunks[0] == b"X-Test: 123\r\n"
    assert chunks[1] == b'\r\n\r\n'
    # suppressed message
    assert chunks[2] == b'\n'
    assert chunks[3] == b"Suppressed content"


def test_meta_only_no_body_or_headers(tmp_path):
    msg = HTTPMessage(
        headers="",
        metadata="Only meta\r\n",
        body=b""
    )
    opts = OutputOptions(headers=False, body=False, meta=True)
    stream = MetaOnlyStream(msg, opts)
    chunks = list(stream)
    # only metadata with surrounding newlines
    assert chunks == [b"Only meta\r\n", b'\n\n']
