import pytest
from httpie.output.streams import EncodedStream
from httpie.encoding import UTF8
from httpie.models import HTTPMessage, OutputOptions
from httpie.context import Environment
from httpie.utils import parse_content_type_header
from httpie.exceptions import BinarySuppressedError

# Helper HTTPMessage that yields lines
class DummyMessage(HTTPMessage):
    def __init__(self, body: bytes, content_type: str = "text/plain", encoding: str = "utf-8"):
        self.body = body
        self.content_type = content_type
        self.encoding = encoding

    def iter_lines(self, chunk_size: int):
        # split body into lines preserving line endings
        lines = self.body.splitlines(keepends=True)
        for line in lines:
            yield line, b"\n"

def test_encoded_stream_normal_decoding(tmp_path):
    body = b"Hello, world!\nSecond line."
    msg = DummyMessage(body)
    env = Environment(stdout_isatty=False, stdout_encoding="utf-8")
    stream = EncodedStream(env=env, msg=msg)
    # Collect output
    output = b"".join(stream.iter_body())
    assert output == body  # should be unchanged
    # encoding property should be None initially
    assert stream.encoding is None

def test_encoded_stream_binary_suppression(tmp_path):
    body = b"Valid text\x00with null byte"
    msg = DummyMessage(body)
    env = Environment(stdout_isatty=False, stdout_encoding="utf-8")
    stream = EncodedStream(env=env, msg=msg)
    with pytest.raises(BinarySuppressedError):
        list(stream.iter_body())

def test_encoded_stream_encoding_guess(tmp_path):
    # Two lines with same guessed encoding 'latin-1'
    body = "Café\nnaïve".encode("latin-1")
    msg = DummyMessage(body, encoding=None)
    env = Environment(stdout_isatty=False, stdout_encoding="utf-8")
    stream = EncodedStream(env=env, msg=msg)
    # First iteration: no encoding guessed yet
    first = next(stream.iter_body())
    assert stream.encoding is None
    # Second iteration: two guesses same, encoding should be set
    second = next(stream.iter_body())
    assert stream.encoding == "latin-1"
    # Output should be encoded to UTF-8
    assert first == b"Caf\xc3\xa9\n"
    assert second == b"na\xc3\xafve\n"
