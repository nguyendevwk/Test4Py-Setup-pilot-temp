import pytest
import requests
from httpie.models import OutputOptions, RequestsMessageKind, infer_requests_message_kind, OPTION_TO_PARAM
from httpie.cli.constants import (
    OUT_REQ_BODY,
    OUT_REQ_HEAD,
    OUT_RESP_BODY,
    OUT_RESP_HEAD,
    OUT_RESP_META
)

def test_output_options_from_request_message():
    # Create a PreparedRequest instance
    req = requests.Request('GET', 'https://example.com').prepare()
    # raw_args contains only the header flag
    opts = OutputOptions.from_message(req, raw_args=OUT_REQ_HEAD)
    assert opts.kind is RequestsMessageKind.REQUEST
    assert opts.headers is True
    assert opts.body is False
    assert opts.meta is False
    # Ensure that any() reflects the flags
    assert opts.any() is True

def test_output_options_from_response_message_with_all_flags():
    # Create a Response instance
    resp = requests.Response()
    resp.status_code = 200
    resp.url = 'https://example.com'
    # raw_args contains all response flags
    raw = f"{OUT_RESP_HEAD} {OUT_RESP_BODY} {OUT_RESP_META}"
    opts = OutputOptions.from_message(resp, raw_args=raw)
    assert opts.kind is RequestsMessageKind.RESPONSE
    assert opts.headers is True
    assert opts.body is True
    assert opts.meta is True
    assert opts.any() is True

def test_infer_requests_message_kind_invalid_type():
    with pytest.raises(TypeError) as excinfo:
        infer_requests_message_kind(object())
    assert "Unexpected message type" in str(excinfo.value)
