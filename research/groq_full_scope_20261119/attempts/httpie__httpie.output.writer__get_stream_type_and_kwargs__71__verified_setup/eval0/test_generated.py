import pytest
from httpie.output.writer import get_stream_type_and_kwargs
from httpie.context import Environment
from httpie.output.processing import Conversion, Formatting
from httpie.output.streams import (
    RawStream, EncodedStream, PrettyStream, BufferedPrettyStream
)
from httpie.output.models import ProcessingOptions
from httpie.models import HTTPResponse, HTTPMessage
from httpie.cli.dicts import HTTPHeadersDict

def make_env(stdout_isatty: bool):
    """Create a minimal Environment with the desired tty state."""
    env = Environment()
    env.stdout_isatty = stdout_isatty
    return env

def test_pretty_stream_on_tty_with_prettify():
    env = make_env(stdout_isatty=True)
    opts = ProcessingOptions(
        stream=False,
        prettify=None,
        response_mime=None,
        response_charset=None,
        style='default',
        json=False,
        format_options={}
    )
    # Pretend we want prettify groups
    opts.prettify_groups = ['json']
    stream_cls, kwargs = get_stream_type_and_kwargs(
        env, opts, HTTPMessage, HTTPHeadersDict()
    )
    assert stream_cls is PrettyStream
    assert isinstance(kwargs['conversion'], Conversion)
    assert isinstance(kwargs['formatting'], Formatting)
    assert kwargs['formatting'].groups == ['json']

def test_raw_stream_on_non_tty_without_prettify():
    env = make_env(stdout_isatty=False)
    opts = ProcessingOptions(
        stream=False,
        prettify=None,
        response_mime=None,
        response_charset=None,
        style='default',
        json=False,
        format_options={}
    )
    stream_cls, kwargs = get_stream_type_and_kwargs(
        env, opts, HTTPMessage, HTTPHeadersDict()
    )
    assert stream_cls is RawStream
    # chunk_size should be the default (not stream)
    assert kwargs['chunk_size'] == RawStream.CHUNK_SIZE

def test_auto_streaming_from_event_stream_header():
    env = make_env(stdout_isatty=False)
    opts = ProcessingOptions(
        stream=False,
        prettify=None,
        response_mime=None,
        response_charset=None,
        style='default',
        json=False,
        format_options={}
    )
    headers = HTTPHeadersDict({'Content-Type': 'text/event-stream'})
    stream_cls, kwargs = get_stream_type_and_kwargs(
        env, opts, HTTPResponse, headers
    )
    # Should pick RawStream with stream chunk size
    assert stream_cls is RawStream
    assert kwargs['chunk_size'] == RawStream.CHUNK_SIZE_BY_LINE
