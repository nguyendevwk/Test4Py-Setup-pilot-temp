import argparse
import pytest
from httpie.client import make_default_headers, DEFAULT_UA, FORM_CONTENT_TYPE, JSON_ACCEPT, JSON_CONTENT_TYPE

def test_json_headers_when_json_flag_set():
    """When the `--json` flag is set, Accept and Content-Type should be JSON."""
    args = argparse.Namespace(json=True, data=None, form=False, files=None)
    headers = make_default_headers(args)
    assert headers['User-Agent'] == DEFAULT_UA
    assert headers['Accept'] == JSON_ACCEPT
    assert headers['Content-Type'] == JSON_CONTENT_TYPE

def test_auto_json_headers_when_data_provided_and_not_form():
    """When data is provided without `--form`, auto JSON detection should set headers."""
    args = argparse.Namespace(json=False, data='{"key":"value"}', form=False, files=None)
    headers = make_default_headers(args)
    assert headers['Accept'] == JSON_ACCEPT
    assert headers['Content-Type'] == JSON_CONTENT_TYPE

def test_form_headers_without_files():
    """When `--form` is used without files, Content-Type should be form-encoded."""
    args = argparse.Namespace(json=False, data=None, form=True, files=None)
    headers = make_default_headers(args)
    assert headers['Content-Type'] == FORM_CONTENT_TYPE
    # No Accept header should be added for form-only requests
    assert 'Accept' not in headers
