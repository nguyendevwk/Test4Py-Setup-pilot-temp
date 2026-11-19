import argparse
import pytest
from httpie.client import make_default_headers, DEFAULT_UA, FORM_CONTENT_TYPE, JSON_ACCEPT, JSON_CONTENT_TYPE

def test_default_headers_no_data_or_form():
    """When no data or form is provided, only User-Agent should be set."""
    args = argparse.Namespace(data=None, form=False, json=False, files=None)
    headers = make_default_headers(args)
    assert headers == {'User-Agent': DEFAULT_UA}
    assert 'Accept' not in headers
    assert 'Content-Type' not in headers

def test_default_headers_json_auto_and_explicit():
    """When JSON data is sent (either via --json or data without form), Accept and Content-Type are set."""
    # Case 1: explicit --json flag
    args_json = argparse.Namespace(data=None, form=False, json=True, files=None)
    headers_json = make_default_headers(args_json)
    assert headers_json['Accept'] == JSON_ACCEPT
    assert headers_json['Content-Type'] == JSON_CONTENT_TYPE
    assert headers_json['User-Agent'] == DEFAULT_UA

    # Case 2: data provided without form flag
    args_data = argparse.Namespace(data='{"key":"value"}', form=False, json=False, files=None)
    headers_data = make_default_headers(args_data)
    assert headers_data['Accept'] == JSON_ACCEPT
    assert headers_data['Content-Type'] == JSON_CONTENT_TYPE
    assert headers_data['User-Agent'] == DEFAULT_UA

def test_default_headers_form_without_files():
    """When form data is sent without files, Content-Type should be form-encoded."""
    args = argparse.Namespace(data='key=value', form=True, json=False, files=None)
    headers = make_default_headers(args)
    assert headers['Content-Type'] == FORM_CONTENT_TYPE
    assert headers['User-Agent'] == DEFAULT_UA
    assert 'Accept' not in headers
