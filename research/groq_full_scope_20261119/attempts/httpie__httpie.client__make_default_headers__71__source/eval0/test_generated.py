import argparse
import pytest
from httpie.client import make_default_headers
from httpie.cli.dicts import HTTPHeadersDict

def test_auto_json_headers_when_data_and_no_form():
    """When data is provided without form, JSON headers are set."""
    args = argparse.Namespace(
        data="{'key': 'value'}",
        form=False,
        json=False,
        files=None,
    )
    headers = make_default_headers(args)
    assert isinstance(headers, HTTPHeadersDict)
    assert headers['User-Agent']  # UA is always present
    assert headers['Accept'] == 'application/json'
    assert headers['Content-Type'] == 'application/json'

def test_form_headers_when_form_and_no_files():
    """When form is provided and no files, form content type is set."""
    args = argparse.Namespace(
        data=None,
        form=True,
        json=False,
        files=None,
    )
    headers = make_default_headers(args)
    assert isinstance(headers, HTTPHeadersDict)
    assert headers['User-Agent']
    assert headers['Content-Type'] == 'application/x-www-form-urlencoded'

def test_json_flag_overrides_data_and_form():
    """Explicit json flag sets JSON headers regardless of data or form."""
    args = argparse.Namespace(
        data="{'key': 'value'}",
        form=True,
        json=True,
        files=None,
    )
    headers = make_default_headers(args)
    assert isinstance(headers, HTTPHeadersDict)
    assert headers['User-Agent']
    assert headers['Accept'] == 'application/json'
    assert headers['Content-Type'] == 'application/json'
