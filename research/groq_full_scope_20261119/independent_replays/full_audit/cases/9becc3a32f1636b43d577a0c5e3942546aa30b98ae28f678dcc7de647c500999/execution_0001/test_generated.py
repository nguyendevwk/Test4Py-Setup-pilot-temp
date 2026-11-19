import http
import pytest
from httpie.client import max_headers

def test_max_headers_sets_and_restores_value(tmp_path):
    original = http.client._MAXHEADERS
    with max_headers(5):
        assert http.client._MAXHEADERS == 5
    assert http.client._MAXHEADERS == original

def test_max_headers_none_sets_infinite(tmp_path):
    original = http.client._MAXHEADERS
    with max_headers(None):
        assert http.client._MAXHEADERS == float("Inf")
    assert http.client._MAXHEADERS == original

def test_max_headers_restores_after_exception(tmp_path):
    original = http.client._MAXHEADERS
    try:
        with max_headers(3):
            assert http.client._MAXHEADERS == 3
            raise RuntimeError("forced error")
    except RuntimeError:
        pass
    assert http.client._MAXHEADERS == original
