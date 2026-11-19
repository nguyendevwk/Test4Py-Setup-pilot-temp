import pytest
from httpie.output.streams import PrettyStream, BinarySuppressedError
from httpie.models import HTTPMessage, OutputOptions
from httpie.encoding import UTF8
from httpie.context import Environment
from httpie.processing import Conversion, Formatting
from httpie.utils import parse_content_type_header

# Dummy conversion that turns binary into text
class DummyConversion(Conversion):
    def get_converter(self, mime):
        return DummyConverter() if mime == "application/octet-stream" else None

class DummyConverter:
    def convert(self, body_bytes):
        # pretend the binary is a UTF-8 encoded string
        return "application/json", body_bytes.decode("utf-8")

# Dummy formatting that just returns the content unchanged
class DummyFormatting(Formatting):
    def format_headers(self, headers): return headers
    def format_metadata(self, metadata): return metadata
    def format_body(self, content, mime): return content

# Helper to create a message with given body lines
class DummyMessage(HTTPMessage):
    def __init__(self, body_lines, content_type="text/plain"):
        self._body_lines = body_lines
        self.content_type = content_type
        self.encoding = "utf-8"
        self.headers = "HTTP/1.1 200 OK"
        self.metadata = ""

    def iter_lines(self, chunk_size):
        for line in self._body_lines:
            yield line.encode("utf-8"), b"\n"

    def __repr__(self):
        return f"<DummyMessage {self.content_type}>"

def test_prettystream_normal_text(tmp_path):
    msg = DummyMessage([b"hello", b"world"])
    opts = OutputOptions(headers=True, body=True, meta=False)
    stream = PrettyStream(
        conversion=DummyConversion(),
        formatting=DummyFormatting(),
        msg=msg,
        output_options=opts,
        env=Environment(stdout_isatty=False),
    )
    result = b"".join(stream)
    # headers + blank line + body lines + newlines
    assert result.startswith(b"HTTP/1.1 200 OK\r\n\r\n")
    assert b"hello\nworld\n" in result

def test_prettystream_binary_suppressed(tmp_path):
    msg = DummyMessage([b"\x00\x01\x02"])
    opts = OutputOptions(headers=True, body=True, meta=False)
    stream = PrettyStream(
        conversion=DummyConversion(),
        formatting=DummyFormatting(),
        msg=msg,
        output_options=opts,
        env=Environment(stdout_isatty=False),
    )
    with pytest.raises(BinarySuppressedError):
        list(stream.iter_body())

def test_prettystream_converter_used(tmp_path):
    msg = DummyMessage([b"{\"key\":\"value\"}"])
    msg.content_type = "application/octet-stream"
    opts = OutputOptions(headers=True, body=True, meta=False)
    stream = PrettyStream(
        conversion=DummyConversion(),
        formatting=DummyFormatting(),
        msg=msg,
        output_options=opts,
        env=Environment(stdout_isatty=False),
    )
    body_chunks = list(stream.iter_body())
    # After conversion, mime should be application/json and body unchanged
    assert body_chunks == [b"{\"key\":\"value\"}\n"]
