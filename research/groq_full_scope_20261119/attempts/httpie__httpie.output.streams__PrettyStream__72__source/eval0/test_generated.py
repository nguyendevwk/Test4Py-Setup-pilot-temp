import pytest
from httpie.output.streams import PrettyStream
from httpie.encoding import UTF8
from httpie.models import HTTPMessage, OutputOptions
from httpie.processing import Conversion, Formatting
from httpie.context import Environment
from httpie.utils import parse_content_type_header

# Dummy conversion that turns bytes to a string and sets mime to 'text/plain'
class DummyConversion(Conversion):
    def get_converter(self, mime):
        if mime == b"application/octet-stream":
            return self
        return None

    def convert(self, body: bytearray):
        return b"text/plain", body.decode("utf-8")

# Dummy formatting that just returns the input unchanged
class DummyFormatting(Formatting):
    def format_headers(self, headers):
        return "Headers"

    def format_metadata(self, metadata):
        return "Metadata"

    def format_body(self, content, mime):
        return content

# Helper to create an HTTPMessage with given body lines
class DummyMessage(HTTPMessage):
    def __init__(self, body_lines):
        self._body_lines = body_lines
        self.headers = {}
        self.metadata = {}
        self.mime = b"text/plain"

    def iter_lines(self, chunk_size):
        for line in self._body_lines:
            yield line, b"\n"

    def __repr__(self):
        return f"<DummyMessage {self._body_lines!r}>"

def test_iter_body_normal_lines():
    """Test that iter_body yields each line processed correctly."""
    msg = DummyMessage([b"line1", b"line2"])
    stream = PrettyStream(
        conversion=DummyConversion(),
        formatting=DummyFormatting(),
        msg=msg,
        output_encoding=UTF8,
        output_options=OutputOptions(),
        environment=Environment(),
    )
    result = list(stream.iter_body())
    assert result == [b"line1\n", b"line2\n"]

def test_iter_body_with_null_byte_and_converter():
    """Test that a null byte in the first chunk triggers conversion."""
    # First line contains null byte, rest normal
    msg = DummyMessage([b"data\x00", b"rest"])
    stream = PrettyStream(
        conversion=DummyConversion(),
        formatting=DummyFormatting(),
        msg=msg,
        output_encoding=UTF8,
        output_options=OutputOptions(),
        environment=Environment(),
    )
    result = list(stream.iter_body())
    # Converter turns bytes to string "data\x00rest" and mime to text/plain
    assert result == [b"data\x00rest"]

def test_iter_body_null_byte_after_first_chunk_raises():
    """Test that a null byte after the first chunk raises BinarySuppressedError."""
    msg = DummyMessage([b"first", b"second\x00", b"third"])
    stream = PrettyStream(
        conversion=DummyConversion(),
        formatting=DummyFormatting(),
        msg=msg,
        output_encoding=UTF8,
        output_options=OutputOptions(),
        environment=Environment(),
    )
    with pytest.raises(Exception) as excinfo:
        list(stream.iter_body())
    # The exception should be BinarySuppressedError from httpie.output.streams
    from httpie.output.streams import BinarySuppressedError
    assert isinstance(excinfo.value, BinarySuppressedError)
