import pytest
from httpie.output.streams import BufferedPrettyStream, BinarySuppressedError


class DummyMessage:
    """Simple HTTPMessage mock that yields predefined chunks."""
    def __init__(self, chunks):
        self._chunks = chunks

    def iter_body(self, chunk_size):
        for chunk in self._chunks:
            yield chunk


class DummyConverter:
    """Mock converter that changes MIME and returns modified body."""
    def __init__(self, new_mime, transform):
        self.new_mime = new_mime
        self.transform = transform

    def convert(self, body):
        return self.new_mime, self.transform(body)


class DummyConversion:
    """Mock conversion registry."""
    def __init__(self, converter=None):
        self._converter = converter

    def get_converter(self, mime):
        return self._converter


class DummyStream(BufferedPrettyStream):
    """Subclass that injects test dependencies."""
    def __init__(self, msg, conversion, mime, process_body):
        self.msg = msg
        self.conversion = conversion
        self.mime = mime
        self.process_body = process_body


def test_iter_body_returns_processed_text():
    """BufferedPrettyStream should yield processed body for plain text."""
    body = b"Hello, world!"
    msg = DummyMessage([body])
    conversion = DummyConversion()  # no converter
    stream = DummyStream(msg, conversion, "text/plain", lambda b: b.upper())
    result = list(stream.iter_body())
    assert result == [b"HELLO, WORLD!"]


def test_iter_body_raises_on_binary_without_converter():
    """If a null byte is found and no converter exists, raise BinarySuppressedError."""
    body = b"binary\x00data"
    msg = DummyMessage([body])
    conversion = DummyConversion()  # no converter
    stream = DummyStream(msg, conversion, "application/octet-stream", lambda b: b)
    with pytest.raises(BinarySuppressedError):
        list(stream.iter_body())


def test_iter_body_uses_converter_when_present():
    """When a converter is available, it should be applied before processing."""
    body = b"json data"
    msg = DummyMessage([body])
    converter = DummyConverter("application/json", lambda b: b[::-1])  # reverse bytes
    conversion = DummyConversion(converter)
    stream = DummyStream(msg, conversion, "text/plain", lambda b: b + b"!")
    result = list(stream.iter_body())
    # converter changes mime to application/json and reverses body
    assert stream.mime == "application/json"
    assert result == [b"atad nosj!"]
