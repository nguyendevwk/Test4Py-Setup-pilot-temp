import pytest
from httpie.models import OutputOptions, RequestsMessage, infer_requests_message_kind, OPTION_TO_PARAM
from requests import Request

def _make_request(method="GET", url="http://example.com"):
    """Helper to create a RequestsMessage instance."""
    req = Request(method=method, url=url)
    return req.prepare()

def test_output_options_from_message_basic():
    """Verify that OutputOptions.from_message correctly parses raw_args."""
    message = _make_request()
    raw_args = "-h -b"  # request headers and body
    opts = OutputOptions.from_message(message, raw_args)
    # kind should be inferred correctly
    assert opts.kind == infer_requests_message_kind(message)
    # headers and body flags set, meta default False
    assert opts.headers is True
    assert opts.body is True
    assert opts.meta is False
    # any() should be True because at least one flag is set
    assert opts.any() is True

def test_output_options_from_message_override_kwargs():
    """Verify that keyword arguments override raw_args parsing."""
    message = _make_request()
    raw_args = ""  # no flags
    opts = OutputOptions.from_message(message, raw_args, meta=True, headers=False)
    # headers overridden to False, meta overridden to True
    assert opts.headers is False
    assert opts.body is False
    assert opts.meta is True
    # any() should be True because meta is True
    assert opts.any() is True

def test_output_options_from_message_boundary_no_flags():
    """Verify that when no flags are provided, all booleans are False."""
    message = _make_request()
    raw_args = ""  # empty string, no flags
    opts = OutputOptions.from_message(message, raw_args)
    # All flags should be False
    assert opts.headers is False
    assert opts.body is False
    assert opts.meta is False
    # any() should be False
    assert opts.any() is False
