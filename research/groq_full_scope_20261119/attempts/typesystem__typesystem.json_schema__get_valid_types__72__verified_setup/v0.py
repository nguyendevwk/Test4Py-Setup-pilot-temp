import pytest
from typesystem.json_schema import get_valid_types

def test_get_valid_types_with_mixed_types(tmp_path):
    data = {"type": ["string", "number", "null", "integer"]}
    types, allow_null = get_valid_types(data)
    # "number" should remove "integer" and "null" should set allow_null
    assert types == {"string", "number"}
    assert allow_null is True

def test_get_valid_types_with_empty_type(tmp_path):
    data = {}
    types, allow_null = get_valid_types(data)
    # Default set should exclude "null" and set allow_null to False
    assert types == {"boolean", "object", "array", "number", "string"}
    assert allow_null is False

def test_get_valid_types_invalid_type_value(tmp_path):
    data = {"type": 42}  # invalid type value
    with pytest.raises(TypeError):
        get_valid_types(data)
