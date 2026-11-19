import http
import pytest
from httpie.client import max_headers

def test_max_headers_sets_and_restores_value():
    original = http.client._MAXHEADERS
    new_limit = 5
    with max_headers(new_limit):
        assert http.client._MAXHEADERS == new_limit
    # After exiting the context, the original value should be restored
    assert http.client._MAXHEADERS == original

def test_max_headers_none_sets_infinite_and_restores():
    original = http.client._MAXHEADERS
    with max_headers(None):
        # When limit is None, the context manager sets _MAXHEADERS to float('Inf')
        assert http.client._MAXHEADERS == float('Inf')
    # After exiting the context, the original value should be restored
    assert http.client._MAXHEADERS == original

def test_max_headers_with_zero_limit():
    original = http.client._MAXHEADERS
    with max_headers(0):
        # A limit of 0 is accepted and set as is
        assert http.client._MAXHEADERS == 0
    # After exiting the context, the original value should be restored
    assert http.client._MAXHEADERS == original
