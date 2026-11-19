import pytest
import requests
from httpie.models import OutputOptions, RequestsMessageKind, infer_requests_message_kind
from httpie.cli.constants import (
    OUT_REQ_BODY,
    OUT_REQ_HEAD,
    OUT_RESP_BODY,
    OUT_RESP_HEAD,
    OUT_RESP_META
)

def test_output_options_from_request_message():
    # Create a PreparedRequest with minimal attributes
    req = requests.Request('GET', 'http://example.com').prepare()
    # raw_args contains flags for headers and body
    raw_args = f"{OUT_REQ_HEAD} {OUT_REQ_BODY}"
    opts = OutputOptions.from_message(req, raw_args)
    assert opts.kind is RequestsMessageKind.REQUEST
    assert opts.headers is True
    assert opts.body is True
    assert opts.meta is False
    assert opts.any() is True

def test_output_options_from_response_message_meta_only():
    # Create a Response with minimal attributes
    resp = requests.Response()
    resp.status_code = 200
    resp.url = 'http://example.com'
    # raw_args contains only meta flag
    raw_args = f"{OUT_RESP_META}"
    opts = OutputOptions.from_message(resp, raw_args)
    assert opts.kind is RequestsMessageKind.RESPONSE
    assert opts.headers is False
    assert opts.body is False
    assert opts.meta is True
    assert opts.any() is True

def test_infer_requests_message_kind_invalid_type():
    with pytest.raises(TypeError) as exc:
        infer_requests_message_kind(object())
    assert "Unexpected message type" in str(exc.value)
