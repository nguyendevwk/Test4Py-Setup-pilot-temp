import argparse
import pytest
from httpie.client import make_default_headers
from httpie.cli.dicts import HTTPHeadersDict

# Constants used in the implementation
DEFAULT_UA = "httpie/1.0"
JSON_ACCEPT = "application/json"
JSON_CONTENT_TYPE = "application/json"
FORM_CONTENT_TYPE = "application/x-www-form-urlencoded"

def test_json_header_set_when_json_flag():
    """When the `--json` flag is set, Accept and Content-Type headers are added."""
    args = argparse.Namespace(
        data=None, form=False, json=True, files=None
    )
    headers = make_default_headers(args)
    assert isinstance(headers, HTTPHeadersDict)
    assert headers["User-Agent"] == DEFAULT_UA
    assert headers["Accept"] == JSON_ACCEPT
    assert headers["Content-Type"] == JSON_CONTENT_TYPE

def test_auto_json_header_when_data_and_not_form():
    """When data is provided and not form, auto_json triggers JSON headers."""
    args = argparse.Namespace(
        data="{'key':'value'}", form=False, json=False, files=None
    )
    headers = make_default_headers(args)
    assert headers["Accept"] == JSON_ACCEPT
    assert headers["Content-Type"] == JSON_CONTENT_TYPE

def test_no_content_type_when_form_and_files():
    """When form is true and files are provided, Content-Type should not be set."""
    args = argparse.Namespace(
        data=None, form=True, json=False, files=["file1.txt"]
    )
    headers = make_default_headers(args)
    # Content-Type should not be present because requests will set it
    assert "Content-Type" not in headers
    assert headers["Accept"] != JSON_ACCEPT  # no JSON headers added
