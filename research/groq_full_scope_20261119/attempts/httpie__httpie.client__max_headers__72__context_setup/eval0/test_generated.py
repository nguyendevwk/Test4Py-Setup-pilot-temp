import http.client
import math
import pytest
from httpie.client import max_headers

def test_max_headers_sets_and_restores_value():
    original = http.client._MAXHEADERS
    new_limit = 10
    with max_headers(new_limit):
        assert http.client._MAXHEADERS == new_limit
    # After exiting the context, the original value should be restored
    assert http.client._MAXHEADERS == original

def test_max_headers_with_none_sets_infinite_and_restores():
    original = http.client._MAXHEADERS
    with max_headers(None):
        # When limit is None, the context manager sets _MAXHEADERS to float('Inf')
        assert http.client._MAXHEADERS == float('Inf')
    # After exiting the context, the original value should be restored
    assert http.client._MAXHEADERS == original

def test_max_headers_with_zero_and_negative_limits():
    original = http.client._MAXHEADERS
    # Zero limit should set _MAXHEADERS to 0
    with max_headers(0):
        assert http.client._MAXHEADERS == 0
    # Negative limit should also set _MAXHEADERS to the negative value
    with max_headers(-5):
        assert http.client._MAXHEADERS == -5
    # After exiting the context, the original value should be restored
    assert http.client._MAXHEADERS == original
