import http.client
import pytest
from httpie.client import max_headers

def test_max_headers_sets_and_restores_value(tmp_path):
    # Capture the original value
    original = http.client._MAXHEADERS
    # Use a specific limit
    limit = 50
    with max_headers(limit):
        # Inside the context, the limit should be applied
        assert http.client._MAXHEADERS == limit
    # After exiting, the original value should be restored
    assert http.client._MAXHEADERS == original

def test_max_headers_none_sets_infinite_and_restores(tmp_path):
    original = http.client._MAXHEADERS
    with max_headers(None):
        # None should set to float('Inf')
        assert http.client._MAXHEADERS == float('Inf')
    # Ensure restoration
    assert http.client._MAXHEADERS == original

def test_max_headers_negative_value_restores_on_exception(tmp_path):
    original = http.client._MAXHEADERS
    try:
        with max_headers(-10):
            # Even with a negative limit, the value is set
            assert http.client._MAXHEADERS == -10
            # Raise an exception to test restoration
            raise RuntimeError("test exception")
    except RuntimeError:
        pass
    # After exception, the original value should be restored
    assert http.client._MAXHEADERS == original
