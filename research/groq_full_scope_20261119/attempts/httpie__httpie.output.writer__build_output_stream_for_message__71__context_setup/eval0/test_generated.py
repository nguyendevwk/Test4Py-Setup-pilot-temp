import pytest
import requests
from httpie.context import Environment
from httpie.models import OutputOptions, RequestsMessageKind
from httpie.output.models import ProcessingOptions
from httpie.output.writer import build_output_stream_for_message, get_stream_type_and_kwargs
from httpie.output.streams import RawStream, EncodedStream, PrettyStream, BufferedPrettyStream

# Helper to create a minimal Environment
def make_env(stdout_isatty=True):
    env = Environment()
    env.stdout_isatty = stdout_isatty
    return env

# Helper to create a minimal OutputOptions
def make_output_options(kind, body=True, meta=False):
    return OutputOptions(kind=kind, body=body, meta=meta)

# Helper to create a minimal ProcessingOptions
def make_processing_options(stream=False, prettify_groups=None):
    po = ProcessingOptions()
    po.stream = stream
    po.get_prettify = lambda env: prettify_groups or []
    po.response_mime = None
    po.response_charset = None
    po.style = None
    po.json = False
    po.format_options = {}
    return po

# Test that a request message yields an EncodedStream and no separator
def test_build_output_stream_for_request():
    env = make_env(stdout_isatty=True)
    req = requests.Request('GET', 'http://example.com').prepare()
    output_options = make_output_options(RequestsMessageKind.REQUEST)
    processing_options = make_processing_options()
    stream_gen = build_output_stream_for_message(env, req, output_options, processing_options)
    streams = list(stream_gen)
    # Should yield exactly one stream object
    assert len(streams) == 1
    assert isinstance(streams[0], EncodedStream)
    # No separator should be appended for requests
    assert all(isinstance(s, EncodedStream) for s in streams)

# Test that a response message with a text/event-stream header yields a BufferedPrettyStream and separator
def test_build_output_stream_for_streaming_response():
    env = make_env(stdout_isatty=True)
    resp = requests.Response()
    resp.status_code = 200
    resp._content = b'event: message\n'
    resp.headers['Content-Type'] = 'text/event-stream'
    output_options = make_output_options(RequestsMessageKind.RESPONSE, body=True, meta=False)
    processing_options = make_processing_options()
    stream_gen = build_output_stream_for_message(env, resp, output_options, processing_options)
    streams = list(stream_gen)
    # Should yield a stream and then a separator
    assert len(streams) == 2
    assert isinstance(streams[0], BufferedPrettyStream)
    assert streams[1] == b'\n\n'

# Test that an invalid kind raises a KeyError
def test_build_output_stream_invalid_kind():
    env = make_env()
    req = requests.Request('GET', 'http://example.com').prepare()
    output_options = OutputOptions(kind='INVALID', body=True, meta=False)
    processing_options = make_processing_options()
    with pytest.raises(KeyError):
        list(build_output_stream_for_message(env, req, output_options, processing_options))
