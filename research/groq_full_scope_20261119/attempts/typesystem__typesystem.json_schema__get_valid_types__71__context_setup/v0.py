import pytest
from typesystem.json_schema import get_valid_types

def test_single_type_string():
    data = {"type": "string"}
    types, allow_null = get_valid_types(data)
    assert types == {"string"}
    assert allow_null is False

def test_multiple_types_and_null():
    data = {"type": ["null", "integer", "number", "boolean"]}
    types, allow_null = get_valid_types(data)
    # "number" should remove "integer", null should be allowed and removed
    assert types == {"boolean"}
    assert allow_null is True

def test_missing_type_defaults_and_number_handling():
    data = {}
    types, allow_null = get_valid_types(data)
    # default set excludes integer when number present
    assert types == {"boolean", "object", "array", "string"}
    assert allow_null is False
