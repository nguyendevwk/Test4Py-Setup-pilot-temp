import pytest
from httpie.output.writer import get_stream_type_and_kwargs
from httpie.output.streams import (
    RawStream, EncodedStream, PrettyStream, BufferedPrettyStream
)
from httpie.models import HTTPResponse, HTTPRequest
from httpie.context import Environment
from httpie.output.processing import Conversion, Formatting
from httpie.output.models import ProcessingOptions
from httpie.cli.dicts import HTTPHeadersDict


class DummyProcessingOptions(ProcessingOptions):
    """Minimal stub for ProcessingOptions used in tests."""
    def __init__(self, stream=False, response_mime=None, response_charset=None,
                 style=None, json=False, format_options=None):
        self.stream = stream
        self.response_mime = response_mime
        self.response_charset = response_charset
        self.style = style
        self.json = json
        self.format_options = format_options or {}

    def get_prettify(self, env):
        # Return a non-empty list to trigger prettify logic
        return ['default'] if self.style else []

    def __repr__(self):
        return f"<DummyProcessingOptions stream={self.stream}>"


def test_pretty_stream_with_tty_and_style(tmp_path):
    """When stdout is a tty and style is set, a PrettyStream is returned."""
    env = Environment(stdout_isatty=True)
    opts = DummyProcessingOptions(stream=False, style='monokai')
    headers = HTTPHeadersDict()
    stream_cls, kwargs = get_stream_type_and_kwargs(env, opts, HTTPResponse, headers)

    assert stream_cls is PrettyStream
    assert kwargs['env'] is env
    assert kwargs['mime_overwrite'] is None
    assert kwargs['encoding_overwrite'] is None
    assert isinstance(kwargs['conversion'], Conversion)
    assert isinstance(kwargs['formatting'], Formatting)
    assert kwargs['formatting'].color_scheme == 'monokai'


def test_raw_stream_non_tty_no_prettify():
    """When stdout is not a tty and no prettify groups, RawStream is used."""
    env = Environment(stdout_isatty=False)
    opts = DummyProcessingOptions(stream=False, style=None)
    headers = HTTPHeadersDict()
    stream_cls, kwargs = get_stream_type_and_kwargs(env, opts, HTTPRequest, headers)

    assert stream_cls is RawStream
    # chunk_size should be the default (not by line)
    assert kwargs['chunk_size'] == RawStream.CHUNK_SIZE
    # No other kwargs should be present
    assert set(kwargs.keys()) == {'chunk_size'}


def test_auto_streaming_from_content_type():
    """When Content-Type is text/event-stream, auto-streaming is enabled."""
    env = Environment(stdout_isatty=False)
    opts = DummyProcessingOptions(stream=False, style=None)
    headers = HTTPHeadersDict({'Content-Type': 'text/event-stream'})
    stream_cls, kwargs = get_stream_type_and_kwargs(env, opts, HTTPResponse, headers)

    assert stream_cls is RawStream
    # chunk_size should be by line because is_stream is True
    assert kwargs['chunk_size'] == RawStream.CHUNK_SIZE_BY_LINE
