import pytest
from typesystem.base import ValidationError

def test_validation_error_initialization_and_representation():
    errors = {"name": ["required"], "age": ["must be integer"]}
    e = ValidationError(errors)
    assert hasattr(e, "errors")
    assert e.errors == errors
    assert isinstance(e, Exception)
    assert e.args[0] == errors
    error_str = str(e)
    assert "name" in error_str
    assert "required" in error_str
    assert "age" in error_str
    assert "must be integer" in error_str
