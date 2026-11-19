import argparse
import pytest
from httpie.client import make_default_headers
from httpie.cli.dicts import HTTPHeadersDict

# Constants used in the implementation
DEFAULT_UA = "httpie/1.0"
JSON_ACCEPT = "application/json"
JSON_CONTENT_TYPE = "application/json"
FORM_CONTENT_TYPE = "application/x-www-form-urlencoded"

def _make_args(**kwargs) -> argparse.Namespace:
    """Helper to create an argparse.Namespace with default attributes."""
    ns = argparse.Namespace(
        data=None,
        form=False,
        json=False,
        files=None,
        **kwargs
    )
    return ns

def test_default_headers_with_json_data():
    """When data is provided and not form, JSON headers are set."""
    args = _make_args(data="{'key':'value'}")
    headers = make_default_headers(args)
    assert isinstance(headers, HTTPHeadersDict)
    assert headers["User-Agent"] == DEFAULT_UA
    assert headers["Accept"] == JSON_ACCEPT
    assert headers["Content-Type"] == JSON_CONTENT_TYPE

def test_default_headers_with_form_no_files():
    """When form is true and no files, form content type is set."""
    args = _make_args(form=True)
    headers = make_default_headers(args)
    assert headers["User-Agent"] == DEFAULT_UA
    assert headers["Content-Type"] == FORM_CONTENT_TYPE
    # Accept header should not be set for form-only
    assert "Accept" not in headers

def test_default_headers_no_special_flags():
    """When no special flags are set, only User-Agent is present."""
    args = _make_args()
    headers = make_default_headers(args)
    assert headers["User-Agent"] == DEFAULT_UA
    assert len(headers) == 1
