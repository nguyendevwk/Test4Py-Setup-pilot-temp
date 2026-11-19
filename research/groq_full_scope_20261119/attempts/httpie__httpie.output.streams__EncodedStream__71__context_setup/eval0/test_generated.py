import pytest
from httpie.output.streams import EncodedStream
from httpie.context import Environment
from httpie.models import HTTPMessage, OutputOptions
from httpie.encoding import UTF8
from httpie.utils import parse_content_type_header

# Minimal HTTPMessage implementation for testing
class DummyMessage(HTTPMessage):
    def __init__(self, body: bytes, content_type: str = "text/plain", encoding: str = "utf-8"):
        self._body = body
        self.content_type = content_type
        self.encoding = encoding

    def iter_lines(self, chunk_size: int):
        # Yield each line separately with a trailing newline
        for line in self._body.splitlines(True):
            yield line, b'\n'

    def headers(self):
        return b""

    def metadata(self):
        return b""

# Test 1: Normal text body is encoded correctly
def test_encoded_stream_normal_text(tmp_path):
    body = b"Hello\nWorld\n"
    msg = DummyMessage(body, content_type="text/plain; charset=utf-8", encoding="utf-8")
    env = Environment(stdout_isatty=True, stdout_encoding="utf-8")
    options = OutputOptions(headers=False, body=True, meta=False)
    stream = EncodedStream(env=env, msg=msg, output_options=options)
    result = b"".join(stream)
    assert result == body

# Test 2: Binary data triggers BinarySuppressedError
def test_encoded_stream_binary_suppressed(tmp_path):
    body = b"binary\x00data"
    msg = DummyMessage(body, content_type="application/octet-stream", encoding="utf-8")
    env = Environment(stdout_isatty=True, stdout_encoding="utf-8")
    options = OutputOptions(headers=False, body=True, meta=False)
    stream = EncodedStream(env=env, msg=msg, output_options=options)
    with pytest.raises(Exception) as excinfo:
        list(stream)
    # The exception should be BinarySuppressedError
    from httpie.output.streams import BinarySuppressedError
    assert isinstance(excinfo.value, BinarySuppressedError)

# Test 3: Encoding guess updates after threshold
def test_encoded_stream_encoding_guess(tmp_path):
    # Simulate a message where smart_decode returns different guesses
    class GuessMessage(DummyMessage):
        def __init__(self, body, guesses):
            super().__init__(body)
            self._guesses = guesses
            self._index = 0

        def iter_lines(self, chunk_size: int):
            for line in self._body.splitlines(True):
                yield line, b'\n'

        def decode_chunk(self, raw_chunk):
            # Override to return a guess
            guess = self._guesses[self._index % len(self._guesses)]
            self._index += 1
            return raw_chunk.decode(guess)

    body = b"test\n"
    guesses = ["utf-8", "utf-8", "utf-8"]
    msg = GuessMessage(body, guesses)
    env = Environment(stdout_isatty=True, stdout_encoding="utf-8")
    options = OutputOptions(headers=False, body=True, meta=False)
    stream = EncodedStream(env=env, msg=msg, output_options=options)
    # Consume first two chunks; encoding should still be None
    list(stream.iter_body())
    assert stream.encoding is None
    # Consume third chunk; encoding should now be set to 'utf-8'
    list(stream.iter_body())
    assert stream.encoding == "utf-8"
