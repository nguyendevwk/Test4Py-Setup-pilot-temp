import io
import pytest
from httpie.context import Environment
from httpie.models import OutputOptions, RequestsMessageKind
from httpie.output.models import ProcessingOptions
from httpie.output.writer import build_output_stream_for_message, MESSAGE_SEPARATOR_BYTES
from httpie.output.streams import RawStream, EncodedStream, PrettyStream, BufferedPrettyStream
from httpie.models import HTTPRequest, HTTPResponse
from requests.models import Response, PreparedRequest


def _make_requests_message(kind: RequestsMessageKind, body: bytes = b"", headers: dict = None):
    """Create a minimal RequestsMessage-like object for testing."""
    if kind == RequestsMessageKind.REQUEST:
        msg = PreparedRequest()
        msg.body = body
        msg.headers = headers or {}
    else:
        msg = Response()
        msg._content = body
        msg.headers = headers or {}
    # Add attribute used in writer
    setattr(msg, "is_body_upload_chunk", False)
    return msg


def test_build_output_stream_for_response_non_tty_raw_stream():
    """When stdout is not a tty and no prettify groups, a RawStream is used."""
    env = Environment(stdout_isatty=False)
    output_options = OutputOptions(kind=RequestsMessageKind.RESPONSE, body=True, meta=False)
    processing_options = ProcessingOptions(stream=False, json=False, style=None, format_options=None)
    requests_message = _make_requests_message(RequestsMessageKind.RESPONSE, body=b"ok", headers={"Content-Type": "text/plain"})

    stream_gen = build_output_stream_for_message(env, requests_message, output_options, processing_options)
    stream = next(stream_gen)
    assert isinstance(stream, RawStream)
    # RawStream should yield the body directly
    assert stream.msg.body == b"ok"
    # No separator should be yielded because stdout_isatty is False
    with pytest.raises(StopIteration):
        next(stream_gen)


def test_build_output_stream_for_request_tty_encoded_stream():
    """When stdout is a tty and request kind, EncodedStream is used."""
    env = Environment(stdout_isatty=True)
    output_options = OutputOptions(kind=RequestsMessageKind.REQUEST, body=True, meta=False)
    processing_options = ProcessingOptions(stream=False, json=False, style=None, format_options=None)
    requests_message = _make_requests_message(RequestsMessageKind.REQUEST, body=b"data", headers={"Content-Type": "application/json"})

    stream_gen = build_output_stream_for_message(env, requests_message, output_options, processing_options)
    stream = next(stream_gen)
    assert isinstance(stream, EncodedStream)
    # EncodedStream should wrap the message and produce encoded output
    # The encoded output should contain the original body
    encoded = stream.msg.body
    assert encoded == b"data"
    # No separator should be yielded because meta is False and body is present
    with pytest.raises(StopIteration):
        next(stream_gen)


def test_build_output_stream_for_response_with_pretty_and_separator():
    """When prettify groups are present, a PrettyStream is used and a separator is yielded."""
    env = Environment(stdout_isatty=True)
    output_options = OutputOptions(kind=RequestsMessageKind.RESPONSE, body=True, meta=False)
    # Pretend we have a prettify group
    processing_options = ProcessingOptions(stream=False, json=False, style=None, format_options=None)
    processing_options.get_prettify = lambda env: ["json"]  # mock prettify groups
    requests_message = _make_requests_message(RequestsMessageKind.RESPONSE, body=b'{"key":"value"}', headers={"Content-Type": "application/json"})

    stream_gen = build_output_stream_for_message(env, requests_message, output_options, processing_options)
    stream = next(stream_gen)
    assert isinstance(stream, PrettyStream)
    # The stream should produce the pretty-printed JSON
    pretty_output = stream.msg.body
    assert b'"key"' in pretty_output
    # After the stream, a separator should be yielded
    separator = next(stream_gen)
    assert separator == MESSAGE_SEPARATOR_BYTES
    with pytest.raises(StopIteration):
        next(stream_gen)
