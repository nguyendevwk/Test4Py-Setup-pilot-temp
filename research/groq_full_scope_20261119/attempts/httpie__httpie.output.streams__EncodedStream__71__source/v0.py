import pytest
from httpie.output.streams import EncodedStream
from httpie.models import HTTPMessage, OutputOptions
from httpie.context import Environment
from httpie.encoding import UTF8


class DummyMessage(HTTPMessage):
    def __init__(self, body: bytes, content_type: str = "text/plain", encoding: str = "utf-8"):
        self._body = body
        self.content_type = content_type
        self.encoding = encoding

    def iter_lines(self, chunk_size: int):
        # Yield each line with its line feed
        for line in self._body.splitlines(True):
            yield line, b"\n"


def test_encoded_stream_normal_output(tmp_path):
    body = b"Hello, world!\nSecond line."
    msg = DummyMessage(body)
    env = Environment(stdout_isatty=False, stdout_encoding="utf-8")
    stream = EncodedStream(env=env, msg=msg)
    output = b"".join(stream.iter_body())
    assert output == body + b"\n"


def test_encoded_stream_binary_suppression():
    body = b"Valid text\x00with null byte"
    msg = DummyMessage(body)
    env = Environment(stdout_isatty=False, stdout_encoding="utf-8")
    stream = EncodedStream(env=env, msg=msg)
    with pytest.raises(Exception) as excinfo:
        list(stream.iter_body())
    assert "BinarySuppressedError" in str(excinfo.value)


def test_encoded_stream_encoding_guess(tmp_path):
    # Two lines with different encodings; second line repeats same encoding
    line1 = "Café".encode("latin-1")
    line2 = "Café".encode("latin-1")
    body = line1 + b"\n" + line2 + b"\n"
    msg = DummyMessage(body, encoding=None)
    env = Environment(stdout_isatty=False, stdout_encoding="utf-8")
    stream = EncodedStream(env=env, msg=msg)
    # First iteration: no encoding guessed yet
    first = next(stream.iter_body())
    assert first == line1 + b"\n"
    # Second iteration: encoding guessed twice, should be set
    second = next(stream.iter_body())
    assert second == line2 + b"\n"
    # After two guesses, encoding should be set to latin-1
    assert stream.encoding == "latin-1"
