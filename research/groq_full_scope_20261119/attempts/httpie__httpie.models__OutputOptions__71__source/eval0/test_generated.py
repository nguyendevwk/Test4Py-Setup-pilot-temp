import pytest
import requests
from httpie.models import OutputOptions, infer_requests_message_kind, OPTION_TO_PARAM
from httpie.models import RequestsMessageKind

def test_from_message_response_parses_raw_args_and_kind():
    # Create a dummy Response object
    resp = requests.Response()
    resp.status_code = 200
    resp._content = b'{"ok":true}'
    resp.headers['Content-Type'] = 'application/json'

    # raw_args contains 'head' and 'body'
    raw_args = 'head body'
    opts = OutputOptions.from_message(resp, raw_args)

    # The kind should be inferred as RESPONSE
    assert opts.kind == RequestsMessageKind.RESPONSE

    # The mapping for RESPONSE should include OUT_RESP_HEAD and OUT_RESP_BODY
    # Ensure that the flags are set accordingly
    assert opts.headers is True
    assert opts.body is True
    assert opts.meta is False

def test_from_message_request_overrides_with_kwargs():
    # Create a dummy Request object
    req = requests.Request('GET', 'http://example.com')
    # raw_args contains only 'head'
    raw_args = 'head'
    # Override body to False via kwargs
    opts = OutputOptions.from_message(req, raw_args, body=False)

    # The kind should be inferred as REQUEST
    assert opts.kind == RequestsMessageKind.REQUEST

    # The mapping for REQUEST should include OUT_REQ_HEAD
    assert opts.headers is True
    # body should be overridden to False
    assert opts.body is False
    # meta should remain default False
    assert opts.meta is False

def test_any_method_returns_correct_boolean():
    # Create a dummy Response object
    resp = requests.Response()
    resp.status_code = 200

    # No raw_args, no kwargs: all flags False
    opts = OutputOptions.from_message(resp)
    assert opts.any() is False

    # Set headers flag via raw_args
    opts = OutputOptions.from_message(resp, raw_args='head')
    assert opts.any() is True
    assert opts.headers is True
    assert opts.body is False
    assert opts.meta is False

    # Set meta flag via kwargs
    opts = OutputOptions.from_message(resp, meta=True)
    assert opts.any() is True
    assert opts.meta is True
