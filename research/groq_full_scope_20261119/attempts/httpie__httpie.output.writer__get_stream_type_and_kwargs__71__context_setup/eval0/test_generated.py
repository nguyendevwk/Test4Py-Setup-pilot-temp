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

# Helper to create a minimal Environment with a given stdout_isatty flag
def make_env(stdout_isatty: bool):
    env = Environment()
    env.stdout_isatty = stdout_isatty
    return env

# 1. Test that when stdout is a TTY and prettify groups are requested,
#    the function returns a PrettyStream (or BufferedPrettyStream) with
#    the correct conversion and formatting kwargs.
def test_pretty_stream_with_tty_and_prettify(tmp_path):
    env = make_env(stdout_isatty=True)
    # Pretend we want to prettify JSON
    processing_options = ProcessingOptions(
        stream=False,
        response_mime=None,
        response_charset=None,
        style=None,
        json=True,
        format_options={},
        prettify_groups=['json']
    )
    headers = HTTPHeadersDict()
    stream_class, kwargs = get_stream_type_and_kwargs(
        env, processing_options, HTTPResponse, headers
    )
    # Since prettify_groups is non-empty, we expect a PrettyStream
    assert stream_class is PrettyStream
    # Check that conversion and formatting are present
    assert isinstance(kwargs['conversion'], Conversion)
    assert isinstance(kwargs['formatting'], Formatting)
    # Formatting should have the same groups and json flag as passed
    assert kwargs['formatting'].groups == ['json']
    assert kwargs['formatting'].explicit_json is True

# 2. Test that when stdout is not a TTY and no prettify groups are requested,
#    the function returns a RawStream with the correct chunk size based on
#    whether streaming is enabled.
def test_raw_stream_non_tty_no_prettify(tmp_path):
    env = make_env(stdout_isatty=False)
    processing_options = ProcessingOptions(
        stream=False,
        response_mime=None,
        response_charset=None,
        style=None,
        json=False,
        format_options={},
        prettify_groups=[]
    )
    headers = HTTPHeadersDict()
    stream_class, kwargs = get_stream_type_and_kwargs(
        env, processing_options, HTTPResponse, headers
    )
    assert stream_class is RawStream
    # Since stream is False, chunk_size should be RawStream.CHUNK_SIZE
    assert kwargs['chunk_size'] == RawStream.CHUNK_SIZE

# 3. Test that when a response has a Content-Type of 'text/event-stream',
#    auto-streaming is enabled even if the user did not request it.
def test_auto_streaming_from_content_type(tmp_path):
    env = make_env(stdout_isatty=False)
    processing_options = ProcessingOptions(
        stream=False,
        response_mime=None,
        response_charset=None,
        style=None,
        json=False,
        format_options={},
        prettify_groups=[]
    )
    headers = HTTPHeadersDict({'Content-Type': 'text/event-stream'})
    stream_class, kwargs = get_stream_type_and_kwargs(
        env, processing_options, HTTPResponse, headers
    )
    # Auto-streaming should trigger RawStream with stream chunk size
    assert stream_class is RawStream
    assert kwargs['chunk_size'] == RawStream.CHUNK_SIZE_BY_LINE
