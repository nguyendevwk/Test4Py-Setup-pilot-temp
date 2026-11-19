import pytest
from httpie.output.streams import BufferedPrettyStream, BinarySuppressedError


class DummyMessage:
    """A minimal HTTPMessage stub that yields predefined chunks."""
    def __init__(self, chunks):
        self._chunks = chunks

    def iter_body(self, chunk_size):
        for chunk in self._chunks:
            yield chunk


class DummyConverter:
    """A minimal converter that returns a new MIME type and body."""
    def __init__(self, new_mime, new_body):
        self.new_mime = new_mime
        self.new_body = new_body

    def convert(self, body):
        return self.new_mime, self.new_body


class DummyConversion:
    """A minimal conversion stub that can return a converter or None."""
    def __init__(self, converter):
        self._converter = converter

    def get_converter(self, mime):
        return self._converter


class TestBufferedPrettyStream(BufferedPrettyStream):
    """A test harness for BufferedPrettyStream that allows injection of dependencies."""
    def __init__(self, msg, conversion, mime, process_body=lambda b: b):
        self.msg = msg
        self.conversion = conversion
        self.mime = mime
        self.process_body = process_body


def test_iter_body_no_null_bytes_yields_processed_body():
    """When the body contains no null bytes and no converter is needed,
    iter_body should yield the processed body unchanged."""
    body = b"Hello, world!"
    msg = DummyMessage([body])
    conversion = DummyConversion(None)
    stream = TestBufferedPrettyStream(msg, conversion, "text/plain")
    result = list(stream.iter_body())
    assert result == [body]


def test_iter_body_with_null_bytes_and_converter():
    """When the body contains null bytes and a converter is available,
    iter_body should use the converter and yield the converted body."""
    original_body = b"binary\x00data"
    converted_body = b"converted text"
    msg = DummyMessage([original_body])
    converter = DummyConverter("text/plain", converted_body)
    conversion = DummyConversion(converter)
    stream = TestBufferedPrettyStream(msg, conversion, "application/octet-stream")
    result = list(stream.iter_body())
    assert result == [converted_body]
    assert stream.mime == "text/plain"


def test_iter_body_with_null_bytes_no_converter_raises():
    """When the body contains null bytes and no converter is available,
    iter_body should raise BinarySuppressedError."""
    body = b"binary\x00data"
    msg = DummyMessage([body])
    conversion = DummyConversion(None)
    stream = TestBufferedPrettyStream(msg, conversion, "application/octet-stream")
    with pytest.raises(BinarySuppressedError):
        list(stream.iter_body())
