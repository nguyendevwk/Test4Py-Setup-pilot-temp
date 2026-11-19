import pytest
from httpie.output.streams import EncodedStream
from httpie.encoding import UTF8
from httpie.models import HTTPMessage, OutputOptions
from httpie.context import Environment
from httpie.utils import parse_content_type_header

# Helper message that yields lines
class DummyMessage(HTTPMessage):
    def __init__(self, body: bytes, content_type: str = "text/plain", encoding: str = "utf-8"):
        self._body = body
        self.content_type = content_type
        self.encoding = encoding

    def iter_lines(self, chunk_size: int):
        # split body into lines
        for line in self._body.splitlines(keepends=True):
            yield line, b"\n"

def test_encoded_stream_normal_decoding(tmp_path):
    body = b"Hello, world!\nSecond line."
    msg = DummyMessage(body)
    env = Environment(stdout_isatty=False, stdout_encoding="utf-8")
    stream = EncodedStream(env=env, msg=msg)
    # Collect output
    output = b"".join(stream.iter_body())
    assert output == body + b"\n"  # original bytes plus newline
    # Ensure output_encoding is message encoding
    assert stream.output_encoding == "utf-8"

def test_encoded_stream_binary_suppression():
    body = b"Valid text\x00with null byte"
    msg = DummyMessage(body)
    env = Environment(stdout_isatty=False, stdout_encoding="utf-8")
    stream = EncodedStream(env=env, msg=msg)
    with pytest.raises(Exception) as excinfo:
        list(stream.iter_body())
    # The exception should be BinarySuppressedError from the module
    assert excinfo.type.__name__ == "BinarySuppressedError"

def test_encoded_stream_encoding_guess(tmp_path):
    # Two lines with same guessed encoding
    body = "Line one\nLine two".encode("latin-1")
    msg = DummyMessage(body, encoding="latin-1")
    env = Environment(stdout_isatty=False, stdout_encoding="utf-8")
    stream = EncodedStream(env=env, msg=msg)
    # Force enough guesses by iterating twice
    list(stream.iter_body())
    # After two guesses, encoding should be set to latin-1
    assert stream.encoding == "latin-1"
    # Subsequent decoding should use the guessed encoding
    output = b"".join(stream.iter_body())
    assert output == body + b"\n"
