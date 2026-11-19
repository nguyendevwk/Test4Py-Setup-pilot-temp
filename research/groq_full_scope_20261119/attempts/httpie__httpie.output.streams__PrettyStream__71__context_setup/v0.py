import pytest
from httpie.output.streams import PrettyStream, BinarySuppressedError
from httpie.models import HTTPMessage, OutputOptions
from httpie.encoding import UTF8
from httpie.processing import Conversion, Formatting
from httpie.context import Environment
from httpie.utils import parse_content_type_header

# Helper message that yields lines
class DummyMessage(HTTPMessage):
    def __init__(self, body: bytes, headers: str = "", metadata: str = "", content_type: str = "text/plain"):
        self._body = body
        self._headers = headers
        self._metadata = metadata
        self._content_type = content_type
        self._encoding = "utf-8"

    def iter_lines(self, chunk_size):
        # split body into lines preserving line endings
        lines = self._body.splitlines(keepends=True)
        for line in lines:
            lf = b"\n" if line.endswith(b"\n") else b""
            yield line.rstrip(b"\n"), lf

    @property
    def headers(self):
        return self._headers

    @property
    def metadata(self):
        return self._metadata

    @property
    def content_type(self):
        return self._content_type

    @property
    def encoding(self):
        return self._encoding

# Dummy conversion that simply returns the same mime and body
class DummyConversion(Conversion):
    def get_converter(self, mime):
        return self

    def convert(self, body: bytes):
        return mime, body.decode("utf-8")

# Dummy formatting that returns unchanged content
class DummyFormatting(Formatting):
    def format_headers(self, headers):
        return headers

    def format_metadata(self, metadata):
        return metadata

    def format_body(self, content, mime):
        return content

@pytest.fixture
def env():
    return Environment(stdout_isatty=False, stdout_encoding=UTF8)

def test_prettystream_text_body(env):
    body = b"hello\nworld\n"
    msg = DummyMessage(body)
    opts = OutputOptions(headers=True, body=True, meta=False)
    stream = PrettyStream(
        conversion=DummyConversion(),
        formatting=DummyFormatting(),
        env=env,
        msg=msg,
        output_options=opts,
    )
    chunks = list(stream)
    # headers + blank line + body lines
    assert chunks[0] == b""
    assert chunks[1] == b"\r\n\r\n"
    assert chunks[2] == b"hello\n"
    assert chunks[3] == b"world\n"

def test_prettystream_binary_suppression(env):
    body = b"binary\x00data\n"
    msg = DummyMessage(body)
    opts = OutputOptions(headers=True, body=True, meta=False)
    stream = PrettyStream(
        conversion=DummyConversion(),
        formatting=DummyFormatting(),
        env=env,
        msg=msg,
        output_options=opts,
    )
    with pytest.raises(BinarySuppressedError):
        list(stream.iter_body())

def test_prettystream_converter_used(env):
    body = b"convert\x00data\n"
    msg = DummyMessage(body)
    opts = OutputOptions(headers=True, body=True, meta=False)
    stream = PrettyStream(
        conversion=DummyConversion(),
        formatting=DummyFormatting(),
        env=env,
        msg=msg,
        output_options=opts,
    )
    # The first line contains null, so converter should be invoked
    chunks = list(stream.iter_body())
    # After conversion, body should be processed as string
    assert chunks == [b"convertdata\n"]
