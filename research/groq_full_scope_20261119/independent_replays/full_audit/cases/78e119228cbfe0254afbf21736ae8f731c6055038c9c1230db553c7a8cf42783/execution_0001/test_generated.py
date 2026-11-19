import http
import pytest
from httpie.client import max_headers

def test_max_headers_sets_and_restores_value(tmp_path):
    original = http.client._MAXHEADERS
    with max_headers(5):
        assert http.client._MAXHEADERS == 5
    # After exiting the context, the original value should be restored
    assert http.client._MAXHEADERS == original

def test_max_headers_with_none_sets_infinite(tmp_path):
    original = http.client._MAXHEADERS
    with max_headers(None):
        # float('Inf') is used when limit is falsy
        assert http.client._MAXHEADERS == float('Inf')
    assert http.client._MAXHEADERS == original

def test_max_headers_multiple_nested_calls(tmp_path):
    original = http.client._MAXHEADERS
    with max_headers(10):
        assert http.client._MAXHEADERS == 10
        with max_headers(20):
            assert http.client._MAXHEADERS == 20
        # After inner context, outer limit should be restored
        assert http.client._MAXHEADERS == 10
    # After all contexts, original value should be restored
    assert http.client._MAXHEADERS == original
