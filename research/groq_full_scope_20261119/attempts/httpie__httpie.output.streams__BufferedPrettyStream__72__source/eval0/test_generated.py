import pytest
from httpie.output.streams import BufferedPrettyStream, BinarySuppressedError

# Dummy classes to simulate required interfaces
class DummyMsg:
    def __init__(self, chunks):
        self._chunks = chunks

    def iter_body(self, chunk_size):
        for chunk in self._chunks:
            yield chunk

class DummyConverter:
    def __init__(self, new_mime, new_body):
        self.new_mime = new_mime
        self.new_body = new_body

    def convert(self, body):
        return self.new_mime, self.new_body

class DummyConversion:
    def __init__(self, converter_map):
        self.converter_map = converter_map

    def get_converter(self, mime):
        return self.converter_map.get(mime)

# Test normal text body without null bytes and no converter
def test_iter_body_normal_text():
    msg = DummyMsg([b'hello ', b'world'])
    conversion = DummyConversion({})
    stream = BufferedPrettyStream.__new__(BufferedPrettyStream)
    stream.msg = msg
    stream.conversion = conversion
    stream.mime = 'text/plain'
    stream.process_body = lambda b: b.upper()
    result = list(stream.iter_body())
    assert result == [b'HELLO WORLD']

# Test binary body that should raise BinarySuppressedError
def test_iter_body_binary_suppressed():
    msg = DummyMsg([b'abc\x00def'])
    conversion = DummyConversion({})
    stream = BufferedPrettyStream.__new__(BufferedPrettyStream)
    stream.msg = msg
    stream.conversion = conversion
    stream.mime = 'application/octet-stream'
    stream.process_body = lambda b: b
    with pytest.raises(BinarySuppressedError):
        list(stream.iter_body())

# Test body that triggers a converter and changes mime
def test_iter_body_with_converter():
    msg = DummyMsg([b'{"key":"value"}'])
    converter = DummyConverter('application/json', b'{"key":"converted"}')
    conversion = DummyConversion({'application/json': converter})
    stream = BufferedPrettyStream.__new__(BufferedPrettyStream)
    stream.msg = msg
    stream.conversion = conversion
    stream.mime = 'application/json'
    stream.process_body = lambda b: b[::-1]  # reverse bytes
    result = list(stream.iter_body())
    # After conversion, mime should be updated and body reversed
    assert stream.mime == 'application/json'
    assert result == [b'}detcernoc":"yek"{']
