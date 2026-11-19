import pytest
from typesystem.json_schema import get_valid_types

def test_get_valid_types_with_various_type_entries():
    # Case 1: type as a single string
    data = {"type": "string"}
    types, allow_null = get_valid_types(data)
    assert types == {"string"}
    assert allow_null is False

    # Case 2: type as a list including null and number
    data = {"type": ["null", "number", "integer", "boolean"]}
    types, allow_null = get_valid_types(data)
    # number should override integer, null should be removed
    assert types == {"number", "boolean"}
    assert allow_null is True

    # Case 3: type omitted, defaults to all primitive types
    data = {}
    types, allow_null = get_valid_types(data)
    assert types == {"boolean", "object", "array", "number", "string"}
    assert allow_null is False

def test_get_valid_types_with_empty_and_nonstandard_inputs():
    # Empty type list should default to all primitive types
    data = {"type": []}
    types, allow_null = get_valid_types(data)
    assert types == {"boolean", "object", "array", "number", "string"}
    assert allow_null is False

    # Type list containing only null should result in all primitives and allow_null True
    data = {"type": ["null"]}
    types, allow_null = get_valid_types(data)
    assert types == {"boolean", "object", "array", "number", "string"}
    assert allow_null is True

def test_get_valid_types_raises_on_invalid_input():
    # Passing a non-dict should raise an AttributeError because .get is not defined
    with pytest.raises(AttributeError):
        get_valid_types(42)
