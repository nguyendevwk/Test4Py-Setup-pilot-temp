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
    """Mock converter that replaces MIME type and returns modified body."""
    def __init__(self, new_mime, transform):
        self.new_mime = new_mime
        self.transform = transform

    def convert(self, body_bytes):
        return self.new_mime, self.transform(body_bytes)


class DummyConversion:
    """Mock conversion registry."""
    def __init__(self, converter_map):
        self.converter_map = converter_map

    def get_converter(self, mime):
        return self.converter_map.get(mime)


class DummyStream(BufferedPrettyStream):
    """Subclass to allow manual attribute injection."""
    def __init__(self, msg, conversion, mime, process_body):
        self.msg = msg
        self.conversion = conversion
        self.mime = mime
        self.process_body = process_body


def test_iter_body_normal_text():
    """Body contains only text; no null bytes and no converter."""
    body = b"Hello, world!"
    msg = DummyMessage([body])
    conversion = DummyConversion({})
    stream = DummyStream(msg, conversion, "text/plain", lambda b: b.upper())
    result = list(stream.iter_body())
    assert result == [b"HELLO, WORLD!"]


def test_iter_body_binary_raises():
    """Body contains a null byte and no converter; should raise BinarySuppressedError."""
    body = b"binary\x00data"
    msg = DummyMessage([body])
    conversion = DummyConversion({})
    stream = DummyStream(msg, conversion, "application/octet-stream", lambda b: b)
    with pytest.raises(BinarySuppressedError):
        list(stream.iter_body())


def test_iter_body_with_converter():
    """Body contains a null byte but a converter is available; conversion applied."""
    body = b"data\x00with\x00nulls"
    msg = DummyMessage([body])
    # Converter will replace MIME and reverse the bytes
    converter = DummyConverter("text/reversed", lambda b: b[::-1])
    conversion = DummyConversion({"application/octet-stream": converter})
    stream = DummyStream(msg, conversion, "application/octet-stream", lambda b: b)
    result = list(stream.iter_body())
    # After conversion, MIME should be updated and body reversed
    assert stream.mime == "text/reversed"
    assert result == [b"slunnw\x00atad"]
