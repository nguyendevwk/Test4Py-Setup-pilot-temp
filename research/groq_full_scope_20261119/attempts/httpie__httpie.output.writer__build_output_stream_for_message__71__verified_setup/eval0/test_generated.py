import io
import pytest
import requests
from httpie.context import Environment
from httpie.models import (
    HTTPRequest,
    HTTPResponse,
    HTTPMessage,
    RequestsMessage,
    RequestsMessageKind,
    OutputOptions,
)
from httpie.output.models import ProcessingOptions
from httpie.output.writer import build_output_stream_for_message
from httpie.output.streams import MESSAGE_SEPARATOR_BYTES


def _make_env(isatty: bool = True) -> Environment:
    """Create a minimal Environment with the requested stdout_isatty flag."""
    env = Environment()
    env.stdout_isatty = isatty
    return env


def _make_requests_message(kind: RequestsMessageKind, body: bytes = b"", headers: dict = None):
    """Create a RequestsMessage of the given kind with optional body and headers."""
    if kind == RequestsMessageKind.REQUEST:
        req = requests.Request(method="GET", url="http://example.com")
        prepped = req.prepare()
        prepped.body = body
        prepped.headers = headers or {}
        return RequestsMessage(prepped, kind=kind)
    else:
        resp = requests.Response()
        resp.status_code = 200
        resp._content = body
        resp.headers = headers or {}
        return RequestsMessage(resp, kind=kind)


def test_build_output_stream_for_request_body_and_meta(tmp_path):
    """Normal case: request with body and meta output."""
    env = _make_env(isatty=False)
    req_msg = _make_requests_message(
        RequestsMessageKind.REQUEST,
        body=b"payload",
        headers={"Content-Type": "text/plain"},
    )
    output_options = OutputOptions(kind=RequestsMessageKind.REQUEST, body=True, meta=True)
    processing_options = ProcessingOptions()
    stream = io.BytesIO()
    for chunk in build_output_stream_for_message(
        env, req_msg, output_options, processing_options
    ):
        stream.write(chunk)
    data = stream.getvalue()
    # The output should contain the request line and the body
    assert b"GET http://example.com" in data
    assert b"payload" in data
    # Meta information (headers) should also be present
    assert b"Content-Type: text/plain" in data


def test_build_output_stream_for_response_no_body_no_meta(tmp_path):
    """Boundary case: response with no body and no meta output."""
    env = _make_env(isatty=True)
    resp_msg = _make_requests_message(
        RequestsMessageKind.RESPONSE,
        body=b"",
        headers={"Content-Type": "application/json"},
    )
    output_options = OutputOptions(kind=RequestsMessageKind.RESPONSE, body=False, meta=False)
    processing_options = ProcessingOptions()
    stream = io.BytesIO()
    for chunk in build_output_stream_for_message(
        env, resp_msg, output_options, processing_options
    ):
        stream.write(chunk)
    data = stream.getvalue()
    # Only the status line should be present
    assert b"200 OK" in data
    # No body or headers should appear
    assert b"Content-Type" not in data
    # Since stdout_isatty is True but body is False, no separator should be added
    assert MESSAGE_SEPARATOR_BYTES not in data


def test_build_output_stream_invalid_kind_raises():
    """Error case: passing an unsupported RequestsMessageKind should raise KeyError."""
    env = _make_env()
    req_msg = _make_requests_message(RequestsMessageKind.REQUEST)
    # Create an OutputOptions with an invalid kind (e.g., a dummy enum value)
    class DummyKind:
        pass
    output_options = OutputOptions(kind=DummyKind, body=True, meta=False)
    processing_options = ProcessingOptions()
    with pytest.raises(KeyError):
        list(build_output_stream_for_message(env, req_msg, output_options, processing_options))
