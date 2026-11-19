import pytest
from httpie.output.streams import EncodedStream
from httpie.context import Environment
from httpie.models import HTTPMessage, OutputOptions
from httpie.encoding import UTF8

class DummyMessage(HTTPMessage):
    def __init__(self, body: bytes, content_type: str = "text/plain", encoding: str = "utf-8"):
        self._body = body
        self.content_type = content_type
        self.encoding = encoding

    def iter_lines(self, chunk_size=1):
        # Yield each line with its line feed
        for line in self._body.splitlines(True):
            yield line, b'\n'

    def headers(self):
        return b""

    def metadata(self):
        return b""

def test_encoded_stream_normal_text(tmp_path):
    body = b"Hello\nWorld\n"
    msg = DummyMessage(body)
    env = Environment(stdout_isatty=True, stdout_encoding="utf-8")
    stream = EncodedStream(env=env, msg=msg, output_options=OutputOptions(body=True))
    chunks = list(stream)
    # Expect headers not present, body lines encoded in utf-8
    assert chunks == [b"Hello\n", b"World\n"]

def test_encoded_stream_binary_suppressed(tmp_path):
    body = b"Binary\x00Data\n"
    msg = DummyMessage(body)
    env = Environment(stdout_isatty=True, stdout_encoding="utf-8")
    stream = EncodedStream(env=env, msg=msg, output_options=OutputOptions(body=True))
    with pytest.raises(Exception) as excinfo:
        list(stream)
    # The exception should be BinarySuppressedError
    assert excinfo.type.__name__ == "BinarySuppressedError"

def test_encoded_stream_output_encoding_default(tmp_path):
    body = b"Hello\n"
    msg = DummyMessage(body, encoding="iso-8859-1")
    env = Environment(stdout_isatty=False, stdout_encoding="utf-8")
    stream = EncodedStream(env=env, msg=msg, output_options=OutputOptions(body=True))
    chunks = list(stream)
    # Since stdout_isatty is False, output_encoding should preserve message encoding
    assert chunks == [b"Hello\n"]
