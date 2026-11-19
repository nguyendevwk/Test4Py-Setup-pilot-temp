import pytest
from httpie.output.streams import PrettyStream
from httpie.encoding import UTF8
from httpie.models import HTTPMessage, OutputOptions
from httpie.context import Environment
from httpie.utils import parse_content_type_header

# Minimal stubs for dependencies
class DummyFormatting:
    def format_headers(self, headers):
        return f"Headers: {headers}"
    def format_metadata(self, metadata):
        return f"Metadata: {metadata}"
    def format_body(self, content, mime):
        # simply return content unchanged
        return content

class DummyConversion:
    def __init__(self, converter=None):
        self._converter = converter
    def get_converter(self, mime):
        return self._converter

class DummyConverter:
    def convert(self, body_bytes):
        # pretend to decode bytes to string and change mime
        return ("text/plain", body_bytes.decode("utf-8"))

class DummyMessage(HTTPMessage):
    def __init__(self, body_lines, headers=None, metadata=None):
        super().__init__(headers or {}, metadata or {})
        self._body_lines = body_lines
    def iter_lines(self, chunk_size):
        for line in self._body_lines:
            yield line, b"\n"

def test_normal_line_processing(tmp_path):
    # Prepare a message with two text lines
    body = [b"Hello", b"World"]
    msg = DummyMessage(body)
    stream = PrettyStream(
        conversion=DummyConversion(),
        formatting=DummyFormatting(),
        msg=msg,
        output_encoding=UTF8,
        mime="text/plain",
    )
    # Headers and metadata should be formatted correctly
    assert stream.get_headers() == b"Headers: {'Content-Type': 'text/plain'}"
    assert stream.get_metadata() == b"Metadata: {}"
    # Body should be processed line by line
    result = list(stream.iter_body())
    assert result == [b"Hello\n", b"World\n"]

def test_binary_suppressed_error(tmp_path):
    # Message contains a binary line with null byte
    body = [b"Good\x00bye", b"Next"]
    msg = DummyMessage(body)
    stream = PrettyStream(
        conversion=DummyConversion(),
        formatting=DummyFormatting(),
        msg=msg,
        output_encoding=UTF8,
        mime="application/octet-stream",
    )
    with pytest.raises(Exception) as excinfo:
        list(stream.iter_body())
    # The exception should be BinarySuppressedError from httpie.output.streams
    from httpie.output.streams import BinarySuppressedError
    assert isinstance(excinfo.value, BinarySuppressedError)

def test_converter_used_and_body_processed(tmp_path):
    # Message starts with a binary line containing null byte, triggering converter
    body = [b"\x00\x01\x02", b"Rest"]
    msg = DummyMessage(body)
    converter = DummyConverter()
    stream = PrettyStream(
        conversion=DummyConversion(converter=converter),
        formatting=DummyFormatting(),
        msg=msg,
        output_encoding=UTF8,
        mime="application/octet-stream",
    )
    # The converter should convert the entire body to a string
    result = list(stream.iter_body())
    # After conversion, the body should be a single string chunk followed by newline
    assert result == [b"Hello World\n"]  # DummyConverter returns decoded string "Hello World"
