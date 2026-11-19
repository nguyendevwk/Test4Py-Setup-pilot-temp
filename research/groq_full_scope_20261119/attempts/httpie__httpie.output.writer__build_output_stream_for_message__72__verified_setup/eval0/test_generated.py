import builtins
import types
import pytest
from httpie.output.writer import build_output_stream_for_message, get_stream_type_and_kwargs
from httpie.context import Environment
from httpie.models import (
    HTTPRequest,
    HTTPResponse,
    RequestsMessageKind,
    OutputOptions,
)
from httpie.output.models import ProcessingOptions

# Helper dummy stream that yields a single string
class DummyStream:
    def __init__(self, msg, output_options, **kwargs):
        self.msg = msg
        self.output_options = output_options
        self.kwargs = kwargs

    def __iter__(self):
        yield f"streamed:{self.msg.__class__.__name__}:{self.output_options.kind}"

# Dummy RequestsMessage with minimal attributes
class DummyRequestsMessage:
    def __init__(self, kind, headers=None):
        self.kind = kind
        self.headers = headers or {}
        # attribute used in build_output_stream_for_message
        self.is_body_upload_chunk = False

# Dummy Environment
class DummyEnvironment(Environment):
    def __init__(self, stdout_isatty=True):
        super().__init__()
        self.stdout_isatty = stdout_isatty

# Dummy OutputOptions
class DummyOutputOptions(OutputOptions):
    def __init__(self, kind, body=True, meta=False):
        super().__init__(kind=kind, body=body, meta=meta)

# Dummy ProcessingOptions
class DummyProcessingOptions(ProcessingOptions):
    def __init__(self):
        super().__init__()

@pytest.fixture
def patch_get_stream():
    """Patch get_stream_type_and_kwargs to return DummyStream."""
    original = get_stream_type_and_kwargs
    def fake_get_stream_type_and_kwargs(*args, **kwargs):
        return DummyStream, {}
    yield fake_get_stream_type_and_kwargs
    # restore not needed as test module ends

def test_build_output_stream_for_request(patch_get_stream):
    env = DummyEnvironment(stdout_isatty=False)
    req_msg = DummyRequestsMessage(kind=RequestsMessageKind.REQUEST)
    out_opts = DummyOutputOptions(kind=RequestsMessageKind.REQUEST)
    proc_opts = DummyProcessingOptions()

    gen = build_output_stream_for_message(env, req_msg, out_opts, proc_opts)
    result = list(gen)
    # Should yield one stream output, no separator because stdout_isatty is False
    assert result == ["streamed:HTTPRequest:REQUEST"]

def test_build_output_stream_for_response_with_separator(patch_get_stream):
    env = DummyEnvironment(stdout_isatty=True)
    resp_msg = DummyRequestsMessage(kind=RequestsMessageKind.RESPONSE)
    out_opts = DummyOutputOptions(kind=RequestsMessageKind.RESPONSE, body=True, meta=False)
    proc_opts = DummyProcessingOptions()

    gen = build_output_stream_for_message(env, resp_msg, out_opts, proc_opts)
    result = list(gen)
    # Should yield stream output followed by separator bytes
    assert result[0] == "streamed:HTTPResponse:RESPONSE"
    assert result[1] == b"\n"

def test_build_output_stream_with_extra_kwargs(patch_get_stream):
    env = DummyEnvironment(stdout_isatty=False)
    req_msg = DummyRequestsMessage(kind=RequestsMessageKind.REQUEST)
    out_opts = DummyOutputOptions(kind=RequestsMessageKind.REQUEST)
    proc_opts = DummyProcessingOptions()

    extra = {"foo": "bar"}
    gen = build_output_stream_for_message(env, req_msg, out_opts, proc_opts, extra_stream_kwargs=extra)
    result = list(gen)
    # DummyStream should receive the extra kwarg
    stream_obj = DummyStream(msg=HTTPRequest(req_msg), output_options=out_opts, **extra)
    assert result == [f"streamed:{stream_obj.msg.__class__.__name__}:{stream_obj.output_options.kind}"]
