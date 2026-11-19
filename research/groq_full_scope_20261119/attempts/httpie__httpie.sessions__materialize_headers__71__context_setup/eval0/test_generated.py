import pytest
from httpie.sessions import materialize_headers

def test_materialize_headers_basic_order_and_content(tmp_path):
    # Basic dictionary with multiple headers
    headers = {"Content-Type": "application/json", "Accept": "application/xml"}
    result = materialize_headers(headers)
    # Ensure the result is a list of dicts with correct keys and values
    assert isinstance(result, list)
    assert len(result) == 2
    # Order should match insertion order of the original dict
    assert result[0] == {"name": "Content-Type", "value": "application/json"}
    assert result[1] == {"name": "Accept", "value": "application/xml"}

def test_materialize_headers_empty_dict(tmp_path):
    # Empty dictionary should produce an empty list
    headers = {}
    result = materialize_headers(headers)
    assert result == []

def test_materialize_headers_invalid_input_raises(tmp_path):
    # Passing a non-dict type should raise an AttributeError because .copy() is missing
    with pytest.raises(AttributeError):
        materialize_headers(["Content-Type", "application/json"])
