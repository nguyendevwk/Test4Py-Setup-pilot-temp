import pytest
from typesystem.json_schema import get_valid_types

def test_get_valid_types_with_mixed_types():
    data = {"type": ["string", "number", "integer", "null"]}
    types, allow_null = get_valid_types(data)
    # "number" should remove "integer", "null" should set allow_null and be removed
    assert types == {"string", "number"}
    assert allow_null is True

def test_get_valid_types_with_empty_type():
    data = {}
    types, allow_null = get_valid_types(data)
    # Default set should be returned and null allowed
    assert types == {"boolean", "object", "array", "number", "string"}
    assert allow_null is False

def test_get_valid_types_with_single_string_type():
    data = {"type": "integer"}
    types, allow_null = get_valid_types(data)
    # Single string type should be converted to set
    assert types == {"integer"}
    assert allow_null is False
