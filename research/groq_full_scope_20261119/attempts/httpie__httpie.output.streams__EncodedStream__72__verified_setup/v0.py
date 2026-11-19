import pytest
from httpie.output.streams import EncodedStream
from httpie.models import HTTPMessage, OutputOptions
from httpie.context import Environment
from httpie.encoding import UTF8

# Helper HTTPMessage that yields lines from a given byte string
class DummyMessage(HTTPMessage):
    def __init__(self, body: bytes, content_type: str = "text/plain", encoding: str = None):
        self.body = body
        self.content_type = content_type
        self.encoding = encoding

    def iter_lines(self, chunk_size=1):
        # Yield each line with its linefeed
        for line in self.body.splitlines(True):
            yield line, b"\n"

def test_normal_decoding_and_encoding(tmp_path):
    body = b"Hello, world!\nSecond line."
    msg = DummyMessage(body, encoding="utf-8")
    env = Environment(stdout_isatty=False, stdout_encoding="utf-8")
    stream = EncodedStream(env=env, msg=msg)
    result = b"".join(stream.iter_body())
    assert result == body + b"\n"  # original body with added newline after each line

def test_binary_suppression_raises_error(tmp_path):
    body = b"Valid text\x00with null byte"
    msg = DummyMessage(body, encoding="utf-8")
    env = Environment(stdout_isatty=False, stdout_encoding="utf-8")
    stream = EncodedStream(env=env, msg=msg)
    with pytest.raises(Exception) as excinfo:
        list(stream.iter_body())
    assert "BinarySuppressedError" in str(excinfo.value)

def test_encoding_guess_and_update(tmp_path):
    # Two lines with same guessed encoding 'latin-1'
    body = b"\xC3\xA9\n\xC3\xA9"  # bytes that decode as 'é' in latin-1
    msg = DummyMessage(body, encoding=None)
    env = Environment(stdout_isatty=False, stdout_encoding="utf-8")
    stream = EncodedStream(env=env, msg=msg)
    # First iteration: no encoding guessed yet
    first = next(stream.iter_body())
    assert stream.encoding is None
    # Second iteration: same guess appears twice, encoding should be set
    second = next(stream.iter_body())
    assert stream.encoding == "latin-1"
    # Subsequent iteration should use the set encoding
    third = next(stream.iter_body())
    assert stream.encoding == "latin-1"
