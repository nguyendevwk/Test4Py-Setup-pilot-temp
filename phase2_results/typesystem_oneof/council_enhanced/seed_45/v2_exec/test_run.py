import pytest
from typesystem.composites import OneOf
from typesystem.fields import String, Integer
from typesystem.base import ValidationError

def test_oneof_validation_logic():
    schema = OneOf([String(), Integer()])

    val, err = schema.validate_or_error("hello")
    assert err is None
    assert val == "hello"

    val, err = schema.validate_or_error(42)
    assert err is None
    assert val == 42

    multi_schema = OneOf([String(), String()])
    val, err = multi_schema.validate_or_error("dup")
    assert val is None
    assert isinstance(err, ValidationError)
    assert err.code == "multiple_matches"

    val, err = schema.validate_or_error(None)
    assert val is None
    assert isinstance(err, ValidationError)
    assert err.code == "no_match"

    with pytest.raises(AssertionError):
        OneOf([String()], allow_null=True)
