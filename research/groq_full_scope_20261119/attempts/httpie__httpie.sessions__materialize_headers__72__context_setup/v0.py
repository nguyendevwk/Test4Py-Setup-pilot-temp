import pytest
from httpie.sessions import materialize_headers

def test_materialize_headers_basic():
    headers = {"Content-Type": "application/json", "Accept": "text/plain"}
    result = materialize_headers(headers)
    # Ensure each header is represented as a dict with correct keys
    assert isinstance(result, list)
    assert len(result) == 2
    assert {"name": "Content-Type", "value": "application/json"} in result
    assert {"name": "Accept", "value": "text/plain"} in result

def test_materialize_headers_empty():
    headers = {}
    result = materialize_headers(headers)
    # Empty input should produce an empty list
    assert result == []

def test_materialize_headers_immutable_input():
    headers = {"X-Test": "value"}
    original_copy = headers.copy()
    materialize_headers(headers)
    # The original dictionary should remain unchanged
    assert headers == original_copy
    assert headers is not None
