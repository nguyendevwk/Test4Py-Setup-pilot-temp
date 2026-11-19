import http
import pytest
from httpie.client import max_headers

def test_max_headers_sets_and_restores_value(tmp_path):
    # Capture original value
    original = http.client._MAXHEADERS
    # Use a small limit
    with max_headers(5):
        assert http.client._MAXHEADERS == 5
    # After exiting, original value should be restored
    assert http.client._MAXHEADERS == original

def test_max_headers_none_sets_infinite(tmp_path):
    original = http.client._MAXHEADERS
    with max_headers(None):
        # float('Inf') is used internally
        assert http.client._MAXHEADERS == float('Inf')
    assert http.client._MAXHEADERS == original

def test_max_headers_negative_value(tmp_path):
    original = http.client._MAXHEADERS
    # Negative values are accepted; the context manager does not validate
    with max_headers(-10):
        assert http.client._MAXHEADERS == -10
    assert http.client._MAXHEADERS == original
